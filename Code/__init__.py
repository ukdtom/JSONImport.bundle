##############################################################################
# JSONImporter
# An import agent for medias, where the WebTools JSON Exporter has been run against
#
# Purpose of this agent is to make it easy to more Plex to a new server, regardless of platform
#
# Made by dane22, a Plex Community member
#
# Credits goes to the developers of the Plex Agent named XBMCnfoMoviesImporter, since I shamlessly
# borrowed a few lines of code ;-)
##############################################################################

import os, io, json, datetime
from dateutil.parser import parse

JSONFILEEXT = '.json'
POSTERFILEEnd = '-poster.jpg'
FANARTFILEEnd = '-fanart.jpg'

class jsonimportmovies(Agent.Movies):
	name = 'JSONImporter'
	ver = '1.0.0.0'
	primary_provider = True
	languages = [Locale.Language.English, Locale.Language.Swedish, Locale.Language.French, 
								Locale.Language.Spanish, Locale.Language.Dutch, Locale.Language.German, Locale.Language.Italian, 
								Locale.Language.Danish,Locale.Language.Arabic, Locale.Language.Catalan, Locale.Language.Chinese, 
								Locale.Language.Czech, Locale.Language.Estonian, Locale.Language.Finnish, Locale.Language.Greek, 
								Locale.Language.Hebrew, Locale.Language.Hindi, Locale.Language.Hungarian, Locale.Language.Indonesian, 
								Locale.Language.Japanese, Locale.Language.Korean, Locale.Language.Latvian, Locale.Language.Norwegian, 
								Locale.Language.Persian, Locale.Language.Polish, Locale.Language.Portuguese, Locale.Language.Romanian, 
								Locale.Language.Russian, Locale.Language.Slovak, Locale.Language.Thai, Locale.Language.Turkish, 
								Locale.Language.Ukrainian, Locale.Language.Vietnamese]

	accepts_from = ['com.plexapp.agents.localmedia','com.plexapp.agents.opensubtitles','com.plexapp.agents.podnapisi','com.plexapp.agents.subzero']

##### search function #####
	def search(self, results, media, lang):
		# Grap the medias filename and path
		mediaFile = media.items[0].parts[0].file
		filename = String.Unquote(mediaFile).encode('utf8', 'ignore')
		# Get name of json file
		plexJSON = os.path.splitext(filename)[0] + JSONFILEEXT
		Log.Debug('Name and path to plexJSON file is: ' + plexJSON)
		try:
			if os.path.isfile(plexJSON):
				Log.Debug('%s was found' % plexJSON)
				with io.open(plexJSON) as json_file:
						json_data = json.load(json_file)
				# Loaded okay, so let's check if the json file is our's
				if json_data['About This File'] == 'JSON Export Made with WebTools for Plex':
					Log.Debug('The json file was ours, so lets continue')
					# We simply grap the needed fields now from the json, and if one fails, we continue with the others
					try:
						media.name = json_data['title']
					except:
						pass
					try:
						year = int(json_data['year'])
						media.year = year
					except:
						pass
					try:
						media.id = json_data['guid'].split('//')[1].split('?')[0]
					except:
						pass
					'''
					ord3 = lambda x : '%.3d' % ord(x)
					id = int(''.join(map(ord3, media.name+str(media.year))))
					id = str(abs(hash(int(id))))
					media.id = id
					Log.Debug("ID generated: " + media.id)
					'''
				else:
					Log.Critical('Found json file, but not ours !!!!')
			else:
				Log.Error('%s was not found' % plexJSON)
			Log.Debug('Search returning: Id= %s, title= %s, year= %s' %(media.id, media.name, str(media.year))) 
			results.Append(MetadataSearchResult(id=media.id, name=media.name, year=media.year, lang=lang, score=100))
		except Exception, e:
			Log.Exception('Exception happend in search: %s' % str(e))
	
##### update Function #####
	def update(self, metadata, media, lang):
		Log.Debug('******* STARTING UPDATE ********')
		# Grap the medias filename and path
		mediaFile = media.items[0].parts[0].file
		filename = String.Unquote(mediaFile).encode('utf8', 'ignore')
		# Get name of json file
		plexJSON = os.path.splitext(filename)[0] + JSONFILEEXT
		Log.Debug('Name and path to plexJSON file is: ' + plexJSON)
		try:
			if os.path.isfile(plexJSON):
				Log.Debug('%s was found' % plexJSON)
				with io.open(plexJSON) as json_file:
						json_data = json.load(json_file)
				# Title
				try:
					metadata.title = json_data['title']
				except:
					pass
				# Studio
				try:
					metadata.studio = json_data['studio']
				except:
					pass
				# Summery
				try:
					metadata.summary = json_data['summary']
				except:
					pass
				# tagline
				try:
					tagline = json_data['tagline']
					metadata.tagline = tagline
				except:
					pass
				# Original Title
				try:
					originalTitle = json_data['originalTitle']
					metadata.original_title = originalTitle
				except:
					pass
				# Content Rating
				try:
					contentRating = json_data['contentRating']
					metadata.content_rating = contentRating
				except:
					pass
				# Originally Available At
				try:
					originallyAvailableAt = parse(json_data['originallyAvailableAt'])
					metadata.originally_available_at = originallyAvailableAt
				except:
					pass
				# Year
				try:
					year = int(json_data['year'])
					metadata.year = year
				except:
					pass
				# Duration
				try:
					duration = int(json_data['duration'])
					metadata.duration = duration
				except:
					pass
				# Rating
				try:
					rating = float(json_data['rating'])
					metadata.rating = rating
				except:
					pass
				# Title Sort
				try:
					media.title_sort = json_data['titleSort']
				except:
					pass
				# audienceRatingImage
				try:
					metadata.audience_rating_image = json_data['audienceRatingImage']
				except:
					pass
				# audience_rating
				try:
					metadata.audience_rating = float(json_data['audienceRating'])
				except Exception, e:
					pass
				except:
					pass
				# ratingImage
				try:
					metadata.rating_image = json_data['ratingImage']
				except:
					pass
				# Genres
				try:
					metadata.genres.clear()
					for genre in json_data['Genre']:
						metadata.genres.add(genre)
				except:
					pass			
				''' Not part of the API
				# Label
				metadata.labels.clear()
				for Label in json_data['Label']:
					metadata.labels.add(Label)
				'''
				# Collections
				try:
					metadata.collections.clear()
					for collection in json_data['Collection']:
						metadata.collections.add(collection)
				except:
					pass
				# Countries
				try:
					metadata.countries.clear()
					for country in json_data['Country']:
						metadata.countries.add(country)
				except:
					pass
				# Directors
				try:
					metadata.directors.clear()
					for director in json_data['Director']:
						metadata.directors.new().name = director
				except:
					pass
				# Producers
				try:
					metadata.producers.clear()
					for producer in json_data['Producer']:
						metadata.producers.new().name = producer
				except:
					pass
				# Writers
				try:
					metadata.writers.clear()
					for writer in json_data['Writer']:
						metadata.writers.new().name = writer
				except:
					pass
				# Actors
				try:
					metadata.roles.clear()
					for actor in json_data['Role']:
						role = metadata.roles.new()
						role.name = actor['name']
						role.role = actor['role']
						try:
							role.photo = actor['thumb']
						except:
							pass
				except:
					pass
				# Poster
				try:
					posterFilename = os.path.splitext(filename)[0] + POSTERFILEEnd
					if os.path.isfile(posterFilename):
						# Clean out any existing posters
						for key in metadata.posters.keys():
							del metadata.posters[key]
						posterData = Core.storage.load(posterFilename)
						metadata.posters[posterFilename] = Proxy.Media(posterData)
				except:
					pass
				# FanArt
				try:
					fanArtFilename = os.path.splitext(filename)[0] + FANARTFILEEnd
					if os.path.isfile(fanArtFilename):
						# Clean out any existing backgrounds
						for key in metadata.art.keys():
							del metadata.art[key]
						fanArtData = Core.storage.load(fanArtFilename)
						metadata.art[fanArtFilename] = Proxy.Media(fanArtData)
				except:
					pass
			return metadata		
		except Exception, e:
			Log.Exception('Exception in Update: %s' % str(e))


