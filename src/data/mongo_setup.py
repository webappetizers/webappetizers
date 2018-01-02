import mongoengine

alias = 'core'
db = 'streets_db'

# for production
data = dict(
	username=user_from_config_or_env,
	password=password_from_config_or_env,
	host=server_from_config_or_env,
	port=port_from_config_or_env,
	authentication_source='admin',
	authentication_mechanism='SCRAM-SHA-1',
	ssl=True,
	ssl_cert_reqs=ssl.CERT_NONE,
)

mongoengine.register_connection(alias=alias, name=db, **data)
