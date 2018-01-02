import mongoengine


class Street(mongoengine.Document):
	city = mongoengine.StringField(required=True)
	coords = mongoengine.EmbeddedDoccumentField(Line)
	elevs = mongoengine.EmbeddedDoccumentField(Elevation)
	color = mongoengine.StringField()
	meta = {
		'db_alias': 'core',
		'collection': 'streets'
	}


class Line(mongoengine.EmbeddedDoccument):
	street_id = mongoengine.ObjectIdField()
	lat1 = mongoengine.FloatField(required=True)
	lon1 = mongoengine.FloatField(required=True)
	lat2 = mongoengine.FloatField(required=True)
	lon2 = mongoengine.FloatField(required=True)

	@property
	def avglat(self):
		avglat = (self.lat1 + self.lat2) / 2
		return avglat

	@property
	def avglon(self):
		avglon = (self.lon2 + self.laon2) / 2
		return avglon

class Elevation(mongoengine.EmbeddedDoccument):
	street_id = mongoengine.ObjectIdField()
	elev1 = mongoengine.FloatField()
	elev2 = mongoengine.FloatField()

	@property
	def avgelev(self):
		avgelev = (self.elev1 + self.elev2) / 2
		return avgelev