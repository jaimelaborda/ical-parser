from icalendar import Calendar
import wget
import re

from flask import Flask, send_file
app = Flask(__name__)

#url = 'http://www.upv.es/ical/E212429CBCCCA133BDFC7DC49488D99BC616EC444AC2A7F245F5E62EFBF27C40335E9E56C1FFCB6F'

def icalParser(url):
    # Get the file from the internet
    print("\nDonwloading ical file...")
    filename = wget.download(url)
    #filename = "icalendar-23-08-2019-20-21.ics"

    # Open and Parse the file
    print("\n\nParsing "+filename+"...")

    g = open(filename,'rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            # Get description
            summary = component.get('summary')
            description = component.get('description')
            
            # Parse and get the subject
            description = description.replace("<br/>", "\n")
            description = description.replace("<br>", "\n")
            subject = description.split("</b>")
            subject = subject[0].replace("<b>", "")
            subject = re.sub('\([^()]*\)', '', subject)

            # Set summary to subject + type of class
            component['summary'] = subject+"("+summary+")"
            #print(component['summary'])

            #Set description
            component['description'] = description
            #print(description)
            
    g.close

    g = open(filename, 'wb')
    g.write(gcal.to_ical())
    g.close()

    print("\nCorrectly parsed!. Exiting...")
    return filename


@app.route("/ical/<hash>", methods=['GET'])
def getIcal(hash):
    filename = icalParser('http://www.upv.es/ical/'+hash)
    return send_file(filename, attachment_filename=filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=False, port=5000, host='0.0.0.0')