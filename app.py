################################################################
#  https://techwithtim.net/tutorials/flask/a-basic-website/    #
# https://pythonprogramming.net/practical-flask-introduction/  #
################################################################

from flask import Flask, render_template, redirect, url_for, request, session
from datetime import timedelta
import requests
from string import Template
from datetime import datetime

base_url = ' https://api.gdeltproject.org/api/v2/doc/doc'
geo_base_url = "https://api.gdeltproject.org/api/v2/geo/geo"

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")  # this sets the route to this page
def home():
	#return "Hello! this is the main page <h1>HELLO</h1>"  # some basic inline html
    #return render_template("index.html", content="Testing", n=4)
    return render_template("index.html")

################################################################
# http://localhost:5000/timelinevoltone/covid/china/science
@app.route("/gdeltdocapi", methods=["POST", "GET"])#/<topic>/<sourcecountry>/<theme>")
def gdeltdocapi():#topic, sourcecountry, theme):
    
    # ====================================================
    # QUERY
    # ====================================================
    title = "Search from GDELT DOC 2.0 API"
    msg = ""
    searchterm = None
    domain = None
    sourcecountry = None 
    sourcelang = None
    theme = None
    tone = None
    startdatetime = None
    enddatetime = None
    timespan = None
    mode = None
    format = None
    trans = None
    #st = None
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        #st = request.form.get("searchterm")
        #print("Search term: ", searchterm)

        domain = request.form["domain"]
        #print("Domain: ", domain)

        sourcecountry = request.form["sourcecountry"]
        #print("Source country: ", sourcecountry)

        sourcelang = request.form.get("sourcelang")
        #print("Source lang: ", sourcelang)

        theme = request.form.get("theme")
        print("Theme: ", theme)

        tone = request.form.get("tone")
        #print("Tone:", tone)

        startdatetime = request.form.get("startdatetime")
        #print("Start date: ", startdatetime)

        enddatetime = request.form.get("enddatetime")
        #print("End date: ", enddatetime)

        timespan = request.form.get("timespan")
        if timespan == "":
            timespan = "3months"
        #print("Timespan: ", timespan)

        mode = request.form.get("mode")
        #print("Mode: ", mode)

        format = request.form.get("format")
        #print("Format: ", format)

        trans = request.form.get("trans")
        #print("Trans: ", trans)


    else:
        if searchterm == None:
            return render_template("gdeltdocapi.html")
    
    #searchterm = request.form.get("nm")
    # params = {'query': [topic, "sourcecountry:{}".format(sourcecountry), "theme:{}".format(theme)], 'mode': 'timelinetone'}
    # https://api.gdeltproject.org/api/v2/doc/doc?query=covid&mode=ArtList&maxrecords=75&trans=googtrans&startdatetime=20170101103000&enddatetime=20200817211158
    # https://zhuoyunao.github.io/#api=doc&query=covid&timelinemode=TimelineTone&timelinesmooth=0&startdatetime=20200101000000&enddatetime=20200301235959
    
    params = {}
    query = []
    query.append(searchterm)
    msg = msg + "Search term: " + searchterm + ", "
    if sourcecountry != "":
        sourcecountry = "sourcecountry:"+sourcecountry
        query.append(sourcecountry)
        msg = msg + "Source country: " + sourcecountry + ", "
    if domain != "":
        domain = "domain:"+domain
        query.append(domain)
        msg = msg + "Domain: " + domain + ", "
    if sourcelang != "":
        sourcelang = "sourcelang:"+sourcelang
        query.append(sourcelang)
        msg = msg + "Source lang: " + sourcelang + ", "
    if theme != "":
        theme = "theme:"+theme
        query.append(theme)
        msg = msg + "Theme: " + theme + ", "
    if tone != "":
        query.append(tone)
        msg = msg + "Tone: " + tone + ", "
    
    params['query'] = query
    #print(query)
    params['mode'] = mode #'timelinevolinfo'
    msg = msg + "Mode: " + mode + ", "
    if mode != "artlist":
        params['TIMELINESMOOTH'] = "5"
        msg = msg + "TIMELINESMOOTH: " + "5" + ", "
    params['format'] = format
    msg = msg + "Format: " + format + ", "

    if mode == "artlist": # only translation provided for artlist
        if trans != None:
            params['trans'] = trans
    
    if startdatetime == "" or enddatetime == "":
        if timespan == "":
            timespan = "1w"
        params['timespan'] = timespan
        msg = msg + "Timespan: " + timespan + ", "
    else:
        # work out the date time format: YYYYMMDDHHMMSS
        # from 2020-04-01T12:30
        startdatetime = startdatetime.replace("-", "")
        msg = msg + "Start date: " + startdatetime + ", "
        startdatetime = startdatetime+"000000"
        #print(startdatetime)
        params['startdatetime'] = startdatetime


        enddatetime = enddatetime.replace("-", "")
        msg = msg + "End date: " + enddatetime
        enddatetime = enddatetime+"235959"
        params['enddatetime'] = enddatetime

    params['maxrecords'] = 200 # max up to 250

    
    response = requests.get(base_url, params=params)#, verify=False)
    print(response.url)
    
    theurl = response.url
    #print(msg)
    return render_template("gdeltdocresponse.html", result=theurl, title=title, msg=msg)

####################################################################
# gdeltdeoapi
@app.route("/gdeltgeoapi", methods=["POST", "GET"])
def gdeltgeoapi():
    title = "Search from GDELT GEO 2.0 API"
    msg = ""
    # ====================================================
    # QUERY
    # https://zhuoyunao.github.io/#api=geo&query=covid&geomode=PointData&geotimespan=1d
    # https://zhuoyunao.github.io/#api=geo&query=covid&geomode=PointHeatmap&geoformat=GeoJSON&geotimespan=1d
    # https://zhuoyunao.github.io/#api=geo&query=covid&geomode=PointData&geoformat=html&geotimespan=7d
    # https://zhuoyunao.github.io/#api=geo&query=covid&geomode=PointHeatmap&geoformat=GeoJSON&geotimespan=7d
    # 
    # ====================================================
    searchterm = None
    domain = None
    location = None
    locationcc = None
    sourcecountry = None 
    sourcelang = None
    theme = None
    tone = None
    timespan = None
    mode = None
    format = None
    #maxpoints = 1000
    
    # ================================================
    # Access the form data
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        #print("Search term: ", searchterm)

        domain = request.form["domain"]
        #print("Domain: ", domain)

        location = request.form["location"]
        #print("Location: ", location)

        locationcc = request.form["locationcc"]
        #print("LocationCC: ", locationcc)

        sourcecountry = request.form["sourcecountry"]
        #print("Source country: ", sourcecountry)

        sourcelang = request.form.get("sourcelang")
        #print("Source lang: ", sourcelang)

        theme = request.form.get("theme")
        #print("Theme: ", theme)

        tone = request.form.get("tone")
        #print("Tone:", tone)

        timespan = request.form.get("timespan")
        if timespan == "":
            timespan = "24h" # default
        #print("Timespan: ", timespan)

        mode = request.form.get("mode")
        #print("Mode: ", mode)

        format = request.form.get("format")
        #print("Format: ", format)
 
    else:
        if searchterm == None:
            return render_template("gdeltgeoapi.html")


    # =================================================
    # Setup the URL parameters for the query
    params = {}
    query = []
    query.append(searchterm)
    msg = msg + " " + "Search term: " + searchterm + ", "
    if domain != "":
        domain = "domain:"+domain
        query.append(domain)
        msg = msg + " " + "Domain: " + domain + ", "
    if location != "":
        location = "location:"+location
        query.append(location)
        msg = msg + "Location: " + location + ", "
    if locationcc != "":
        locationcc = "locationcc:"+locationcc
        query.append(locationcc)
        msg = msg + "LocationCC: " + locationcc + ", "
    if sourcecountry != "":
        sourcecountry = "sourcecountry:"+sourcecountry
        query.append(sourcecountry)
        msg = msg + "Source Country: " + sourcecountry + ", "
    if sourcelang != "":
        sourcelang = "sourcelang:"+sourcelang
        query.append(sourcelang)
        msg = msg + "Source language: " + sourcelang + ", "
    if theme != "":
        theme = "theme:"+theme
        query.append(theme)
        msg = msg + "Theme: " + theme + ", "
    if tone != "":
        query.append(tone)
        msg = msg + "Tone: " + tone + ", "
    
    params['query'] = query
    #print(query)
    params['mode'] = mode #'timelinevolinfo'
    msg = msg + "Mode: " + mode + ", "
    params['format'] = format
    msg = msg + "Format: " + format + ", "
    params['timespan'] = timespan
    msg = msg + "timespan: " + timespan

    
    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(geo_base_url, params=params)#, verify=False)
    print(response.url)

    # =================================================
    # Show the result to user
    theurl = response.url
    
    return render_template("gdeltgeoresponse.html", result=theurl, msg=msg, title=title)

####################################################################
# gdeltgkggeojson api 
@app.route("/gdeltgkggeojsonapi", methods=["POST", "GET"])
def gdeltgkggeojsonapi():
    title = "Search from GDELT GKG GEOJSON API"

    # ====================================================
    # QUERY
    # ====================================================
    searchterm = None
    domain = None
    lang = None
    geoname = None
    timespan = None
    outputtype = None
    outputfields = None
    gcamvar = None
    maxrows = None
    #maxpoints = 1000
    
    # ================================================
    # Access the form data
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        print("Search term: ", searchterm)

        domain = request.form["domain"]
        print("Domain: ", domain)

        lang = request.form["lang"]
        print("Language: ", lang)

        geoname = request.form["geoname"]
        print("Geoname: ", geoname)

        timespan = request.form.get("timespan")
        print("Timespan: ", timespan)

        gcamvar = request.form.get("gcamvar")
        print("GCAMVAR: ", gcamvar)

        maxrows = request.form.get("maxrows")
        print("maxrows: ", maxrows)


        outputtype = request.form.get("outputtype")
        print("OUTPUTTYPE: ", outputtype)

        outputfields = request.form.get("outputfields")
        print("OUTPUTFIELDS: ", outputfields)
 
    else:
        if searchterm == None:
            return render_template("gdeltgkggeojsonapi.html")


    # =================================================
    # Setup the URL parameters for the query
    #
    # Feed of all Monitored News Coverage in the Last Hour.
    # https://api.gdeltproject.org/api/v1/gkg_geojson
    #
    # Feed of Food Security Coverage in the Last Hour.  
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=FOOD_SECURITY)
    #
    # Feed of BBC.co.uk Coverage in the Last 24 Hours.
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=domain:bbc.co.uk&TIMESPAN=1440
    # 
    # Feed of Arabic Language Coverage of Last 2 Hours
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=lang:Arabic&TIMESPAN=120
    # 
    # Feed of Arabic Language Coverage of Last 2 Hours With Custom Output Fields
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=lang:Arabic&TIMESPAN=120&OUTPUTFIELDS=url,name,sharingimage,tone,lang
    # 
    # Feed of Anxiety Emotion Over Last Two Hours.  Here we use the special GCAMVAR parameter 
    # to include the RID "Anxiety" emotion assessed through the GDELT GCAM pipeline by 
    # looking up its variable name in the GCAM Master Codebook.
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=&TIMESPAN=120&OUTPUTFIELDS=url,name,sharingimage,tone,lang&GCAMVAR=c8.3
    # 
    # Feed For Animated Map of Anxiety Over Last 24 Hours.
    # https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=&TIMESPAN=1440&OUTPUTFIELDS=tone&GCAMVAR=c8.3&OUTPUTTYPE=2
    #
    # ===================================================
    
    # =============================================
    gkggeojson_url =  "https://api.gdeltproject.org/api/v1/gkg_geojson"

    params = {}
    
    # To search for only Arabic-language FOOD_SECURITY coverage, use the URL 
    # "https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=lang:Arabic,FOOD_SECURITY"
    # Construct query parameter as follows:
    # QUERY=atheme,lang:Arabic,domain:thedomain,geoname:locationname
    # Individual query terms are separated by commas, 
    # words separated by spaces are treated as phrase matches (they should NOT be surrounded by quote marks).

    # =============================================
    # The available parameters are listed below.  
    # Note that they must be specified in all 
    # capital letters.
    # ===============================================

    query = ""
    if searchterm != "":
        query = searchterm
    
    if domain != "":
        if query != "":
            domain = ",domain:"+domain
        else:
            domain = "domain:"+domain
        query = query+domain
    if lang != "":
        if query != "":
            lang = ",lang:"+lang
        else:
            lang = "lang"+lang
        query = query + lang
    if geoname != "":
        if query != "":
            geoname = ",geoname:"+geoname
        else:
            geoname = "geoname:"+geoname
        query = query + geoname
    
    params['QUERY'] = query
    print(query)

    if timespan != "":
        params['TIMESPAN'] = timespan

    if outputtype != "":
        params['OUTPUTTYPE'] = outputtype # "1" for "article", "2" generates "location+time" output

    if len(outputfields) > 0:
        fields = ""
        for i in range(len(outputfields)):
            if fields != "":
                fields = outputfields[i]
            else:
                fields = fields+","+outputfields[i]
        params["OUTPUTFIELDS"] = fields
        print(fields)


    if gcamvar != "":
        params['GCAMVAR'] = gcamvar

    if maxrows != "":
        params['MAXROWS'] = maxrows

    
    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(gkggeojson_url, params=params)#, verify=False)
    print(response.url)

    # =================================================
    # Show the result to user
    theurl = response.url
    
    return render_template("gdeltgkggeojsonresponse.html", result=theurl, title=title)

###########################################################################
# gdelt context api
# =========================================================================
@app.route("/gdeltcontextapi", methods=["POST", "GET"])
def gdeltcontextapi():
    title = "The GDELT Context Search API"

    # ====================================================
    # QUERY
    # ====================================================
    searchterm = None
    domain = None
    isquote = None 
    format = None
    timespan = None
    startdatetime = None
    enddatetime = None
    maxrows = None
    searchlang = None
    sort = None
    
    # ================================================
    # Access the form data
    if request.method == "POST":
        searchterm = request.form["searchterm"]
        print("Search term: ", searchterm)

        domain = request.form["domain"]
        print("Domain: ", domain)

        isquote = request.form["isquote"]
        print("ISQUOTE: ", isquote)

        format = request.form.get("format")
        print("Format: ", format)

        timespan = request.form.get("timespan")
        print("Timespan: ", timespan)

        startdatetime = request.form.get("startdatetime")
        print("Start date: ", startdatetime)

        enddatetime = request.form.get("enddatetime")
        print("End date: ", enddatetime)

        maxrows = request.form.get("maxrows")
        print("MAXROWS: ", maxrows)

        searchlang = request.form.get("searchlang")
        print("SEARCHLANG: ", searchlang)

        sort = request.form.get("sort")
        print("SORT: ", sort)
    
    else:
        if searchterm == None:
            return render_template("gdeltcontextapi.html")

    # ==========================================
    # Construct the request to gdelt context api
    context_url =  "https://api.gdeltproject.org/api/v2/context/context?"

    params = {}

    query = []
    query.append(searchterm)
    
    if domain != "":
        domain = "domain:"+domain
        query.append(domain)
    
    params['query'] = query
    print(query)

    if isquote != "":
        params['isquote'] = isquote
    
    params['mode'] = 'artlist'
    params['format'] = format

    if timespan != "":
        params['timespan'] = timespan
    
    elif startdatetime != "" and enddatetime != "":
        # work out the date time format: YYYYMMDDHHMMSS
        # from 2020-04-01T12:30
        startdatetime = startdatetime.replace("-", "")
        startdatetime = startdatetime+"000000"
        print(startdatetime)
        params['startdatetime'] = startdatetime

        enddatetime = enddatetime.replace("-", "")
        enddatetime = enddatetime+"235959"
        params['enddatetime'] = enddatetime

    if maxrows == "":
        maxrows = 75
    params['maxrecords'] = maxrows

    if searchlang != "":
        params['searchlang'] = searchlang
    if sort != "":
        params['sort'] = sort

    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(context_url, params=params)#, verify=False)
    print(response.url)

    # =================================================
    # Show the result to user
    theurl = response.url
    
    return render_template("contextresponse.html", result=theurl, title=title)

########################################################################
# Stability dashboard API
# ======================================================================
@app.route("/stabilitydashboardapi", methods=["POST", "GET"])
def stabilitydashboardapi():
    title = "The GDELT Stability Dashboard API: Stability Timeline"

    # ====================================================
    # QUERY
    # ====================================================
    msg = ""
    loc = None
    var = None
    output = None 
    timeres = None
    smooth = None
    numdays = None
    mode = None
    autocap = None

    # ================================================
    # Access the form data
    if request.method == "POST":

        loc = request.form["loc"]
        #print("LOC: ", loc)

        var = request.form["var"]
        #print("VAR: ", var)

        output = request.form["output"]
        #print("OUTPUT: ", output)

        timeres = request.form.get("timeres")
        #print("TIMERES: ", timeres)

        smooth = request.form.get("smooth")
        #print("SMOOTH: ", smooth)

        numdays = request.form.get("numdays")
        #print("NUMDAYS: ", numdays)

        mode = request.form.get("MODE")
        #print("MODE: ", mode)

        autocap = request.form.get("autocap")
        #print("AUTOCAP: ", autocap)
        
    else:
        if loc == None:
            return render_template("stabilitydashboardapi.html")

    # ==========================================
    # Construct the request to gdelt stability api
    stabilityendpoint = "https://api.gdeltproject.org/api/v1/dash_stabilitytimeline/dash_stabilitytimeline"
    
    params = {}

    params["LOC"] = loc
    msg = msg + "LOC: " + loc + ", "
    params["VAR"] = var
    msg = msg + "VAR: " + var + ", "
    params["OUTPUT"] = output
    msg = msg + "OUTPUT: " + output + ", "
    params["TIMERES"] = timeres
    msg = msg + "TIMERES: " + timeres + ", "
    params["SMOOTH"] = smooth
    msg = msg + "SMOOTH: " + smooth + ", "
    params["NUMDAYS"] = numdays
    msg = msg + "NUMDAYS: " + numdays + ", "
    if mode == "multi":
        params["MODE"] = mode
        msg = msg + "MODE: " + mode + ", "

    if autocap == "2": # Turn the outlier detetor off
        params["AUTOCAP"] = autocap
        msg = msg + "AUTOCAP: " + autocap 


    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(stabilityendpoint, params=params)#, verify=False)
    print(response.url)

    # =================================================
    # Show the result to user
    theurl = response.url
    
    return render_template("stabilityresponse.html", result=theurl, msg=msg, title=title)

#################################################################
# GDELT Thematic Word Cloud Dashboard API
# ===============================================================
@app.route("/wordclouddashboardapi", methods=["POST", "GET"])
def wordclouddashboardapi():

    title = "The GDELT Thematic Word Cloud Dashboard API"

    # ====================================================
    # QUERY
    # ====================================================
    msg = ""
    loc = None
    var = None
    output = None 
    

    # ================================================
    # Access the form data
    if request.method == "POST":
        
        loc = request.form["loc"]
        #print("LOC: ", loc)

        var = request.form["var"]
        #print("VAR: ", var)

        output = request.form["output"]
        #print("OUTPUT: ", output)

    else:
        if loc == None:
            return render_template("wordclouddashboardapi.html")

    # ==========================================
    # Construct the request to gdelt word cloud dashboard api
    wordcloudendpoint = "https://api.gdeltproject.org/api/v1/dash_thematicwordcloud/dash_thematicwordcloud"
    
    params = {}

    params["LOC"] = loc
    msg = msg + "LOC: " + loc + ", "
    params["VAR"] = var
    msg = msg + "VAR: " + var + ", "
    params["OUTPUT"] = output
    msg = msg + "OUTPUT: " + output

    # =================================================
    # Send the request to GDELT and get the response
    response = requests.get(wordcloudendpoint, params=params)#, verify=False)
    print(response.url)

    # =================================================
    # Show the result to user
    theurl = response.url
    
    return render_template("wordcloudresponse.html", result=theurl, msg=msg, title=title)

######################################################
# /campaign tracker
# ====================================================
@app.route("/campaigntracker")#, methods=["POST", "GET"])
def campaigntracker():

    title = "The GDELT Campaign Tracker Dashboard"

    return render_template("campaigntracker.html", title=title)
    

####################################################
# GDELT SUMMARY: ONLINE NEWS SUMMARY
# /onlinenewssummary
# ===================================================
@app.route("/onlinenewssummary")
def onlinenewssummary():
    title = " The GDELT online news summary"

    #theurl = "https://api.gdeltproject.org/api/v2/summary/summary"
    gdeltsummaryurl = "https://api.gdeltproject.org/api/v2/summary/summary"

    return render_template("onlinenewssummary.html", result=gdeltsummaryurl, title=title)

##################################################
# GDELT SUMMARY: ONLINE NEWS COMPARER
# /onlinenewscomparer
# ================================================
@app.route("/onlinenewscomparer")
def onlinenewscomparer():
    title = "The GDELT online news comparer"
    onlinenewscomparerurl = "https://api.gdeltproject.org/api/v2/summary/summary?d=web&t=compare"

    return render_template("onlinenewscomparer.html", result=onlinenewscomparerurl, title=title)
    
################################################
# Television Explorer
# /tvexplorer
# ===============================================
@app.route("/tvexplorer")
def tvexplorer():
    title = "GDELT Television Explorer"
    tvexplorerurl = "https://api.gdeltproject.org/api/v2/summary/summary?d=iatv"

    return render_template("tvexplorer.html", result=tvexplorerurl, title=title)

#######################################################
# GDELT Query interface on doc and geo api
# /gdeltquery
# =====================================================
@app.route("/gdeltquery")
def gdeltquery():
    title = "GDELT Query Interface based on both DOC 2.o and GEO 2.0 API"
    queryurl = "https://zhuoyunao.github.io"

    return render_template("gdeltquery.html", result=queryurl, title=title)

######################################################## 
# GDELT Live Trends Dashboard
# /livetrendsdashboard
########################################################
@app.route("/livetrendsdashboard")
def livetrendsdashboard():
    title = "GDELT Live Trends Dashboard"
    dashboardurl = "http://live.gdeltproject.org/"

    return render_template("livetrendsdashboard.html", result=dashboardurl, title=title)

####################################################################

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == "__main__":

    #app.run(debug=True)
    # Externally visible server
    app.run(debug=True, host='0.0.0.0')
