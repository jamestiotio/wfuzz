from framework.plugins.api import DiscoveryPlugin
from framework.plugins.api import FuzzResParse
from framework.core.myexception import FuzzException
from externals.moduleman.plugin import moduleman_plugin

import xml.dom.minidom
import urlparse

@moduleman_plugin
class sitemap(DiscoveryPlugin):
    name = "sitemap"
    description = "Parses sitemap.xml file. Optional: discovery.bl=\".txt,.gif\""
    category = ["default", "active", "discovery"]
    priority = 99

    def validate(self, fuzzresult):
	return FuzzResParse.parse_res(fuzzresult).file_fullname == "sitemap.xml" and fuzzresult.code == 200

    def process(self, fuzzresult):
	base_url = fuzzresult.url

	try:
	    dom = xml.dom.minidom.parseString(fuzzresult.history.fr_content())
	except:
	    raise FuzzException(FuzzException.FATAL, 'Error while parsing %s.' % fuzzresult.url)

	urlList = dom.getElementsByTagName("loc")
	for url in urlList:
	    u = url.childNodes[0].data

	    if not self.blacklisted_extension(u) and FuzzResParse.parse_res(fuzzresult).domain == FuzzResParse.parse_url(u).domain:
		self.queue_url(u)

