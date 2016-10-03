import sys
import re

if len(sys.argv) < 3:
    raise Exception("File name not provided")

removeURLs = True
removeFacebook = True
removePhoto = True
removeFacebookMail = True
removeTitle = True  # Remove job title
removeEmpty = True  # Contacts without name and (phone number or email)

matchURL = re.compile("(item\d.URL).*")
matchFacebook = re.compile(".*?(X-SERVICE-TYPE|X-SOCIALPROFILE).*")
matchPhoto = re.compile("PHOTO.*")
matchMail = re.compile("(item\d.)?(EMAIL).*")
matchPhone = re.compile("TEL.*")
matchTitle = re.compile("(TITLE|ORG).*")
matchName = re.compile("^N:(.*)")

contacts = []
with open(sys.argv[1], "rb") as f:
    line = None
    while line != "":  # End of file
        buf = []
        line = f.readline()
        while line != "END:VCARD\r\n" and line != "":
            if line != "BEGIN:VCARD\r\n":
                buf.append(line.rstrip("\n").rstrip("\r"))
            line = f.readline()
        contacts.append(buf)

print len(contacts)

if removeURLs:
    for contact in contacts:
        for n in reversed(range(len(contact))):
            if matchURL.findall(contact[n]) != []:
                contact.pop(n)
                contact.pop(n)
                break

if removeFacebook:
    for contact in contacts:
        for n in reversed(range(len(contact))):
            m = matchFacebook.findall(contact[n])
            if m == ['X-SOCIALPROFILE']:
                contact.pop(n)
                break
            elif m == ['X-SERVICE-TYPE']:
                contact.pop(n)
                contact.pop(n)
                break

if removePhoto:
    for contact in contacts:
        for n in reversed(range(len(contact))):
            m = matchPhoto.findall(contact[n])
            if m != []:
                contact.pop(n)
                while contact[n][0] == " ":
                    contact.pop(n)
                break

if removeFacebookMail:
    for contact in contacts:
        for n in reversed(range(len(contact))):
            m = matchMail.findall(contact[n])
            if m != []:
                if "@facebook.com" in contact[n]:
                    contact.pop(n)
                    contact.pop(n)
                    break

if removeTitle:
    for contact in contacts:
        for n in reversed(range(len(contact))):
            if matchTitle.findall(contact[n]) != []:
                contact.pop(n)
                break

if removeEmpty:
    print "Removed:"
    for m in reversed(range(len(contacts))):
        contact = contacts[m]
        hasTel = False
        hasMail = False
        hasName = False

        for n in reversed(range(len(contact))):
            if not hasName:
                t = matchName.findall(contact[n])
                hasName = t != [] and t[0].replace(";", "") != ""
            if not hasTel:
                hasTel = matchPhone.findall(contact[n])
            if not hasMail:
                hasMail = matchMail.findall(contact[n])

            if hasName and (hasMail or hasTel):
                break

        if not hasName or not(hasMail or hasTel):
            for c in contacts[m]:
                if c[0:2] == "N:":
                    t = filter(lambda x: x != '', c[2:].split(";"))
                    if t == []:
                        pass
                        print "- No Name"
                    else:
                        l = t[0]
                        t.remove(t[0])
                        t.append(l)
                        print "-", " ".join(t)
                    break
            contacts.pop(m)

print len(contacts)

with open(sys.argv[2], "wb") as f:
    for contact in contacts:
        f.write("\n".join(["BEGIN:VCARD"] + contact + ["END:VCARD"]) + "\n")
