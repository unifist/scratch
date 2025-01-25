import json
import unum
import gsheets

class API:

    def __init__(self):
        """ Conencts to gspread using the deaful secret file """

        self.gsheets = gsheets.API()

        with open("/opt/service/config/outreach.json", "r") as outreach_file:
            self.config = json.load(outreach_file)

    def list_listings(self):
        """ List any Listing """

        return self.gsheets.list(f"Outreach Development Admin", "Listings", ["Listing", "Description"])

    def parse_listings(self, listing):

        if "\n" in listing:
            listings = listing.split("\n")
            listings.pop(0)
        else:
            listings = [listing.split(" ", 1)[1]]

        return [listing for listing in listings if len(listing) > 1]


    def create_listing(self, listing):

        description = ""

        if " - " in listing:
            name, description = listing.split(" - ", 1)
        else:
            name = listing

        base = self.gsheets.gspread.open("Outreach Development Base")

        self.gsheets.gspread.copy(base.id, title=f"Outreach Development {name}")
        listing_url = self.gsheets.gspread.open(f"Outreach Development {name}").url

        listings = self.gsheets.gspread.open("Outreach Development Admin").worksheet("Listings")
        listings.append_row([name, description], table_range="A1:B1")

        return listing, listing_url


    def list_categories(self, listing):
        """ List any Categories """

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        return listing, self.gsheets.list(f"Outreach Development {listing}", "Categories", ["Category", "Description"])


    def parse_categories(self, listing_category):

        if "\n" in listing_category:
            categories = listing_category.split("\n")
            listing = categories.pop(0)
        elif " - " in listing_category:
            listing, category = listing_category.split(" - ", 1)
            categories = [category]

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        return (listing, [category for category in categories if len(category) > 1])


    def create_category(self, listing_category):

        listing, category = listing_category.split(" - ", 1)

        description = ""

        if " - " in category:
            name, description = category.split(" - ", 1)
        else:
            name = category

        categories = self.gsheets.gspread.open(f"Outreach Development {listing}").worksheet("Categories")
        categories.append_row([name, description], table_range="A1:B1")

        return listing, category


    def list_resources(self, listing):
        """ List any Resources """

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        return listing, self.gsheets.list(f"Outreach Development {listing}", "Resources", ["Resource", "Description"])


    def parse_resources(self, listing_resource):

        if "\n" in listing_resource:
            resources = listing_resource.split("\n")
            listing = resources.pop(0)
        elif " - " in listing_resource:
            listing, resource = listing_resource.split(" - ", 1)
            resources = [resource]

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        return (listing, [resource for resource in resources if len(resource) > 1])


    def create_resource(self, listing_resource):

        listing, resource = listing_resource.split(" - ", 1)

        description = ""

        if " - " in resource:
            name, description = resource.split(" - ", 1)
        else:
            name = resource

        resources = self.gsheets.gspread.open(f"Outreach Development {listing}").worksheet("Resources")
        resources.append_row([name, description], table_range="A1:B1")

        return listing, resource


    def list_sources(self, listing):
        """ List any Resources """

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        fields = ["Link", "Name", "Status",  "Categories", "Resources", "Description", "Email", "Address", "Phone"]

        return listing, self.gsheets.list(f"Outreach Development {listing}", "Sources", fields)


    def parse_sources(self, listing_catres_source):

        listing, catres_source = listing_catres_source.split(" ", 1)

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        if "\n" in catres_source:
            sources = catres_source.split("\n")
            catres = sources.pop(0)
        elif " - " in catres_source:
            catres, source = catres_source.split(" - ", 1)
            sources = [source]
        else:
            catres, source = catres_source.split("- ", 1)
            sources = [source]

        if catres:

            catres_names = [name.strip() for name in catres.split("+")]

            names = []

            cat_values = self.gsheets.values(f"Outreach Development {listing}", "Categories", "Category")
            res_values = self.gsheets.values(f"Outreach Development {listing}", "Resources", "Resource")
            haystack = cat_values + res_values

            for catres_name in catres_names:
                names.append(unum.closest(haystack, catres_name))

            catres = f"+{' +'.join(names)} "

        return (listing, catres, [source for source in sources if len(source) > 1])


    def create_source(self, listing_catres_source):

        listing, catres_source = listing_catres_source.split(" ", 1)

        listing = self.gsheets.closest("Outreach Development Admin", "Listings", "Listing", listing)

        if "+" in catres_source:
            catres, source = catres_source.split(" - ", 1)
        else:
            catres = ""
            source = catres_source.split("- ")[-1]

        if catres:

            catres_names = catres[1:].split(" +")

            cat_values = self.gsheets.values(f"Outreach Development {listing}", "Categories", "Category")
            res_values = self.gsheets.values(f"Outreach Development {listing}", "Resources", "Resource")

            cat_names = [value for value in cat_values if value in catres_names]
            res_names = [value for value in res_values if value in catres_names]

            categories = ", ".join(cat_names)
            resources = ", ".join(res_names)

        else:

            categories = ""
            resources = ""

        link, name = (source, "") if source.startswith("http") else ("", source)

        row = [link, name, "Found", categories, resources]

        resources = self.gsheets.gspread.open(f"Outreach Development {listing}").worksheet("Sources")
        resources.append_row(row, table_range="A1:E1")

        return listing_catres_source
