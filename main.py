

from flask import Flask, flash, redirect, render_template, request, abort
from LoginManager import LoginManager
if __name__ == "__main__":
    try:
        request_handler = LoginManager()
    except Exception as exc:

        #print traceback.format_exc()
        print (exc)
