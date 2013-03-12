import feedparser
import conf
import PySide.QtNetwork
import codecs
import sys

def setMessage(dialog,i):
    
    # test connection to rss server
    info = PySide.QtNetwork.QHostInfo.fromName(conf.rssHostName)
    sys.stdout = codecs.getwriter('UTF-8')(sys.stdout) 
    
    if info.error() == 0:

        try:
            
            f = feedparser.parse(conf.rssURL)
                    
            messages = len(f['entries'])
            
            header = "<html><body>"
            footer = "</body></html>"
            
            try: 
                title = f['entries'][i]['title']
            except Exception:
                title = 'no title'
            
            try:
                text  = f['entries'][i]['description']
            except Exception:
                text = 'no text'
            
            try:
                link  = '<a href="'+f['entries'][i]['link']+'">Link</a>'
            except Exception:
                link = ''
            
            
            message = header + title + ": <br><br>"+text+"<br>" + link + footer
            
                
        except Exception:
            
            message  = 'Fehler beim Lesen des RSS-Feed \nError reading the RSS-Feed'
    
    elif info.error() ==1:
        
        message  = 'Keine Verbindung mit dem RSS-Feedserver \nno connection with RSS-Feedserver'
        i        = -1
        messages = 0
            
    dialog.ticker.setText(message)
    dialog.messageCounter.setText(str(i+1)+"/"+str(messages))
        
    if i+1 == messages:
        dialog.buttonNext.setDisabled(1)
    else:
        dialog.buttonNext.setDisabled(0)
    
    if i <= 0:
        dialog.buttonPrev.setDisabled(1)
    else:
        dialog.buttonPrev.setDisabled(0)