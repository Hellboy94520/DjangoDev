from ..models.account import AccountAdmin, User
from ..models.localisation import Localisation
from ..models.category import Category
import logging

from .category_portage import create_category_models, reset_category_model
from .localisation_portage import create_localisation_models

import mysql.connector
from mysql.connector import Error
import configparser
import os


logger = logging.getLogger(__name__)


""" ------------------------------------------------------------------------------------------------------------------
AccountAdmin
------------------------------------------------------------------------------------------------------------------ """
def create_portageaccount():
	lAccount = AccountAdmin()
	lAccount.create(username    = "Porting",
	                email       = "alexandre.delahaye@free.fr",
	                password    = "toto",
	                first_name  = "Alex",
	                last_name   = "Delahaye")
	return lAccount


def launch_conversion():
	logging.info("[Portage] Starting...")

	settings = configparser.ConfigParser()
	settings._interpolation = configparser.ExtendedInterpolation()
	if not settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'private/auth_param.ini')):
		logger.fatal("[Portage] Impossible to get the SQL settings".format())

	logging.info("[Portage] Starting SqlClient...")

	try:
		lSqlClient = mysql.connector.connect(host=settings.get('sql_netLiens', 'address'),
		                                     user=settings.get('sql_netLiens', 'user'),
		                                     password=settings.get('sql_netLiens', 'password'),
		                                     database=settings.get('sql_netLiens', 'databasename'))
	except Error as e:
		logging.critical("[SqlClient] Connection cannot be established {}".format(e))
	else:
		lSqlCursor = lSqlClient.cursor()

		# Creation of the AdminAccount
		lPortageAccount = create_portageaccount()

		# Creation of the Category
		# create_category_models(lSqlCursor, lPortageAccount)

		# Creation of the Localisation
		create_localisation_models(settings, lPortageAccount, lSqlCursor)

		# # Creation of the localisation
		# if create_localisation_models(lPortageAccount):
		# 	create_localisation_association(lSqlCursor, lPortageAccount)
		#
		# # Creation of the site
		# create_site_models(lSqlCursor, lPortageAccount)

		lSqlClient.close()

		# Reset useless category data contain in ResumeEn
		reset_category_model(lPortageAccount)
		# reset_localisation_useless_data()

	logging.info("[SqlClient] Connection is closed")
	logging.info("[Portage] Done")
	return True
