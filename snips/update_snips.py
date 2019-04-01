import os
import json
import urllib2
import shutil
import subprocess


SNIPS_URL_TOKEN = 'proj_SNIPS_ID'
EMAIL = 'SNIPS_EMAIL'
PASSWORD = 'SNIPS_PASSWORD'


HOME_DIR = "/home/pi"
SNIPS_CACHE_DIR_NAME = ".snips"
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
SNIPS_CONFIG_PATH="/usr/share/snips"
SNIPS_TEMP_ASSISTANT_FILENAME = "assistant.zip"
SNIPS_TEMP_ASSISTANT_PATH = os.path.join(SNIPS_CACHE_DIR, SNIPS_TEMP_ASSISTANT_FILENAME)
CONSOLE_ASSISTANT_URL = "https://console.snips.ai/api/assistants/{}/download"

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def post_request(url, data, headers):
    raw_data = json.dumps(data)
    req = Request(url, raw_data, headers)
    f = urllib2.urlopen(req)
    info = f.info()
    response = f.read()
    f.close()
    return response, info


def post_request_json(url, data, headers={}):
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    response, info = post_request(url, data, headers)
    return json.loads(response), info


def fetch_url(url, headers=None):
    if headers is None:
        return urlopen(url).read()
    else:
        return urlopen(Request(url, headers=headers)).read()




def prepare_cache():
    if not os.path.exists(HOME_DIR):
        os.makedirs(HOME_DIR)
    if not os.path.exists(SNIPS_CACHE_DIR):
        os.makedirs(SNIPS_CACHE_DIR)

prepare_cache()

def file_exists(file_path):
    return os.path.exists(file_path)

def read_file(file_path):
    if not file_exists(file_path):
        return None
    with open(file_path, "r") as f:
        return f.read()
    return None

def write_text_file(output_file_path, text):
    with open(output_file_path, "w") as f:
        f.write(text)

def remove_file(file_path):
    """ Delete a file.

    :param file_path: the path to the file.
    """
    try:
        os.remove(file_path)
    except OSError:
        pass

class Auth:

    AUTH_URL = "https://external-gateway.snips.ai/v1/user/auth"
  
    @staticmethod
    def retrieve_token(email, password):
        data = { 'email': email, 'password': password }
        response, response_headers = post_request_json(Auth.AUTH_URL, data)
        token = response_headers.getheader('Authorization')
        return token

class Cache:

    STORE_FILE = os.path.join(SNIPS_CACHE_DIR, "token_store")

    @staticmethod
    def get_login_token():
        return read_file(Cache.STORE_FILE)

    @staticmethod
    def save_login_token(token):
        write_text_file(Cache.STORE_FILE, token)
    
    @staticmethod
    def clear_login_token():
        remove_file(Cache.STORE_FILE)


class InvalidTokenException(Exception):
    pass

class Base(object):
    """ The base command. """

    def __init__(self, options, *args, **kwargs):
        """ Initialisation.

        :param options: command-line options.
        :param *args, **kwargs: extra arguments.
        """
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.snipsfile = None

    def run(self):
        """ Command runner. """
        raise NotImplementedError(
            'You must implement the run() method yourself!')

class Login(Base):

    def run(self):
        try:
            Login.login(email=self.options['--email'], password=self.options['--password'])
        except Exception as e:
            print("Error logging in: {}".format(str(e)))


    @staticmethod
    def login(email=None, password=None, greeting=None, silent=False):
        has_credentials = email is not None and password is not None
        silent = silent or has_credentials
        if has_credentials:
            Logout.logout()
        token = Cache.get_login_token()
        
        if not token:
            if not has_credentials:
                print("Please enter your Snips Console credentials")
                email = ask_for_input("Email address:")
                password = ask_for_password("Password:")
            token = Auth.retrieve_token(email, password)
        
            if token is not None:
                Cache.save_login_token(token)
                if not silent:
                    print("You are now signed in")
            else:
                raise InvalidTokenException("Could not validate authentication token")
        else:
            if not silent:
                print("You are already signed in")
        return token


class Logout(Base):

    def run(self):
        if Cache.get_login_token() is not None:
            Logout.logout()
            print("You are now signed out")
        else:
            print("You are already signed out")

    @staticmethod
    def logout():
        Cache.clear_login_token()

class AssistantFetcherException(Exception):
    pass

def write_binary_file(output_file_path, content):
    with open(output_file_path, "wb") as f:
        f.write(content)

def get_assistant_file_path(filename):
        return os.path.join(SNIPS_CACHE_DIR, filename)

def download_console_assistant_only(aid, token):
        url = CONSOLE_ASSISTANT_URL.format(aid)
        return fetch_url(url, headers={'Authorization': token, 'Accept': 'application/json'})

def get_token(email=None, password=None):
        try:
            return Login.login(email=email, password=password, greeting="Please enter your Snips Console credentials to download your assistant.", silent=False)
        except Exception as e:
            raise AssistantFetcherException("Error logging in: {}".format(str(e)))

def execute_command(command):
    """ Execute a shell command.

    :param command: the command to execute.
    :param silent: if True, do not output anything to terminal.
    """
    stdout = open(os.devnull, 'w')
    stderr = open(os.devnull, 'w')

    return subprocess.Popen(command.split(), stdout=stdout, stderr=stderr).communicate()

def copy_local_file(file_path, silent=False):
        if not silent:
            print("Copying assistant {} to {}".format(file_path, SNIPS_TEMP_ASSISTANT_PATH))
        
        error = None
        if not file_exists(file_path):
            error = "Error: failed to locate file {}".format(file_path)
        else:
            try:
                shutil.copy2(file_path, SNIPS_TEMP_ASSISTANT_PATH)
            except Exception as e:
                error = "Error: failed to copy file {}. Make sure you have write permissions to {}".format(file_path, SNIPS_TEMP_ASSISTANT_PATH)

        if error is not None:
            print("error - copy_local_file")
            raise AssistantFetcherException(error)
        else:
            print("done - copy_local_file")
            print("unzipping and installing")
            execute_command("rm -rf " + SNIPS_CONFIG_PATH + "/assistant")
            print("removed old assistant")
            execute_command("rm -rf /var/lib/snips/skills/*")
            print("removed skills")
            execute_command("unzip " + SNIPS_TEMP_ASSISTANT_PATH + " -d " + SNIPS_CONFIG_PATH)
            print("unzipped assistant")
            execute_command("snips-template render")
            print("snips-template render")
            execute_command("systemctl restart 'snips-*'")
            print("restarting snips")
            print("all done")

def download_console_assistant(aid, email=None, password=None, force_download=False):
        token = Cache.get_login_token()
        if token is None:
            token = get_token(email=email, password=password)

        try:
            content = download_console_assistant_only(aid, token)
          
        except Exception as e:
            print("Error Exc: {}".format(str(e)))
            print "ERROR..trying other download"
            Logout.logout()
            token = get_token(email=email, password=password)
            print("Retrying to fetch assistant {} from the Snips Console".format(aid))

            try:
                content = download_console_assistant_only(aid, token)
               
            except Exception:
                print("final error")
                raise AssistantFetcherException("Error fetching assistant from the console. Please make sure the ID is correct, and that you are signed in")

        filepath = get_assistant_file_path("assistant_{}.zip".format(aid))
        print("Saving assistant to {}".format(filepath))
       
        write_binary_file(filepath, content)
       
        copy_local_file(filepath)



download_console_assistant(SNIPS_URL_TOKEN, email=EMAIL, password=PASSWORD)
