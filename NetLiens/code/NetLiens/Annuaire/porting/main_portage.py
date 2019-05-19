from ..models import create_account_admin, AccountAdmin
from ..models.localisation import Localisation, modif_localisation
from django.contrib.auth.models import User
import logging
from ..porting.category_portage     import create_category_models, reset_category_useless_data
from ..porting.localisation_portage import create_localisation_models, create_localisation_association, \
	reset_localisation_useless_data
import mysql.connector
from mysql.connector import Error
import configparser
import os


logger = logging.getLogger(__name__)


""" ------------------------------------------------------------------------------------------------------------------
AccountAdmin
------------------------------------------------------------------------------------------------------------------ """
def create_portageaccount():
	lUser = User.objects.filter(username="Portage")
	if len(lUser) > 0: return AccountAdmin.objects.filter(user=lUser[0])[0]
	else: return create_account_admin("Portage", "", "", "portage@netliens.com", "toto", True)


def launch_conversion():
	logging.info("[Portage] Starting...")

	settings = configparser.ConfigParser()
	settings._interpolation = configparser.ExtendedInterpolation()
	if not settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'private/auth_param.ini')):
		logger.fatal("[Portage] Impossible to get the SQL settings".format())

	logging.info("[Portage] Starting SqlClient...")

	try:
		lSqlClient = mysql.connector.connect(host=settings.get('sql_localhost', 'address'),
		                                     user=settings.get('sql_localhost', 'user'),
		                                     password=settings.get('sql_localhost', 'password'),
		                                     database=settings.get('sql_localhost', 'databasename'))
	except Error as e:
		logging.critical("[SqlClient] Connection cannot be established {}".format(e))
	else:
		lSqlCursor = lSqlClient.cursor()

		# Creation of the data
		lPortageAccount = create_portageaccount()
		create_category_models(lSqlCursor, lPortageAccount)
		if create_localisation_models(lPortageAccount):
			create_localisation_association(lSqlCursor, lPortageAccount)
		lSqlClient.close()

		# Reset useless category data contain in ResumeEn
		reset_category_useless_data()
		reset_localisation_useless_data()

	logging.info("[SqlClient] Connection is closed")
	logging.info("[Portage] Done")
	return True
