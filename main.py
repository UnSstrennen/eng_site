from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from configparser import ConfigParser


config = ConfigParser()
font = config.get("database", "")
print(config.read('config.ini'))