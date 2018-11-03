from enum import Enum
from time import sleep

import vkcore
import cfg
import utils

class post:
    
    def escapeFText(self):
        return utils.escape_string(self.forwarded_text)

    def escapeText(self):
        return utils.escape_string(self.text)

    def __init__(self, input):
        
        if('from_id' in input): self.from_id = input['from_id']
        else: self.from_id = -1

        if('date' in input): self.date = input['date']
        else: self.date = -1

        if('marked_as_ads' in input): self.isAd = input['marked_as_ads'] == 1
        else: self.isAd = False

        if('text' in input): self.text = input['text']
        else: self.text = ''

        if('is_pinned' in input): self.isPinned = input['is_pinned'] == 1
        else: self.isPinned = False

        if('likes' in input and 'count' in input['likes']): self.likeCount = input['likes']['count']
        else: self.likeCount = -1

        if('reposts' in input and 'count' in input['reposts']): self.repostsCount = input['reposts']['count']
        else: self.repostsCount = -1

        if('comments' in input and 'count' in input['comments']): self.commentsCount = input['comments']['count']
        else: self.commentsCount = -1

        if('copy_history' in input):
            self.isForwarded = True

            forward = input['copy_history'][0]

            if('text' in forward): self.forwarded_text = forward['text']
            else: self.forwarded_text = ''

            if('attachments' in forward): 
                if('attachments' in input):
                    input['attachments'].append(forward['attachments'])
                else:
                    input.update( { 'attachments' : forward['attachments'] } )

        else: 
            self.forwarded_text = ''
            self.isForwarded = False

        self.attachments = []
        if('attachments' in input and len(input['attachments']) != 0):
            for attachment in input['attachments']:
                if(attachment['type'] == 'photo' or attachment['type'] == 'posted_photo'):
                    self.attachments.append(photoAttachment(attachment["photo"]))

                elif(attachment['type'] == 'link'):
                    self.attachments.append(linkAttachment(attachment["link"]))

                elif(attachment['type'] == 'doc'):
                    self.attachments.append(docAttachment(attachment["doc"]))

                elif(attachment['type'] == 'video'):
                    self.attachments.append(videoAttachment(attachment["video"]))
                    pass

                elif(attachment['type'] == 'audio'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'graffiti'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'note'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'app'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'poll'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'page'):
                    print('Unknown format {}'.format(attachment['type']))
                else:
                    print('Unknown format {}'.format(attachment['type']))

        pass
    
    def toDebugJSON(self):
        return {
            #"type" : self.type,
            "from_id": self.from_id,
            "date" : self.date,
            "isAd" : self.isAd,
            "isPinned" : self.isPinned,
            #"postSource" : self.postSource,
            "forwarded_text" : (self.forwarded_text[1:50] if len(self.forwarded_text) > 50 else self.forwarded_text) if self.forwarded_text != '' else "<empty>",
            "text" : (self.text[1:50] if len(self.text) > 50 else self.text) if self.text != '' else "<empty>",
            "attachments" : [x.toDebugJSON() for x in self.attachments],
            "likeCount" : self.likeCount,
            "repostsCount" : self.repostsCount,
            "commentsCount" : self.commentsCount  
        }

class attachmentTypes(Enum):
    photo = 1
    video = 2
    doc = 3
    link = 4

class attachment:
    
    def __init__(self, type):
        self.type = type

    def toDebugJSON(self):
        return {
            "type" : self.type
        }

class docAttachment(attachment):

    def __init__(self, input):
        self.type = attachmentTypes.doc

        if('url' in input): self.url = input['url'] 
        else: self.url = ""

        if('type' in input): self.docType = input['type'] 
        else: self.docType = ""

        if('title' in input): self.title = input['title'] 
        else: self.title = ""

        if('ext' in input): self.ext = input['ext'] 
        else: self.ext = ""

        if('size' in input): self.size = input['size'] 
        else: self.size = ""

    def toDebugJSON(self):
        return {
            "type" : self.type,
            "url" : self.url,
            "title" : self.title,
            "ext" : self.ext,
            "size" : self.size
        }

class linkAttachment(attachment):

    def toMarkdown(self):
        return "[{}]({})".format(self.title, self.url)

    def __init__(self, input):
        self.type = attachmentTypes.link

        if('url' in input): self.url = input['url'] 
        else: self.url = ""

        if('title' in input): self.title = input['title'] 
        else: self.title = ""

    def toDebugJSON(self):
        return {
            "type" : self.type,
            "url" : self.url,
            "title" : self.title
        }

class videoAttachment(attachment):

    def getUrl(self):
        return list(self.files.values())[-1]

    def isYouTube(self):
        url = self.getUrl()
        return url.startswith("https://www.youtube.com") or url.startswith("www.youtube.com") or url.startswith("youtu.be")
    
    def __init__(self, input):
        self.type =  attachmentTypes.video

        access_key = input['access_key']
        id = input['id']
        owner_id = input['owner_id']

        sleep(cfg.globalCfg.between_request_delay)
        info = vkcore.get_video(owner_id, id, access_key)
        
        if('duration' in info): self.duration = info['duration']
        else: self.duration = -1

        if('title' in info): self.title = info['title']
        else: self.title = ""

        if('description' in info): self.description = info['description']
        else: self.description = ""

        if('files' in info): self.files = info['files']
        else:  
            self.files = { 'player' : info['player'] }
            #print info['player']
            #files = vkcore.get_video_direct_url(info['player'])
            #print files

    def toDebugJSON(self):
        return {
            "type" : self.type,
            "title" : self.title,
            "description" : self.description,
            "files" : self.files
        }

class photoAttachment(attachment):

    def getUrl(self):
        return self.sizes[-1]

    def __init__(self, input):
        self.type = attachmentTypes.photo

        if('id' in input): self.id = input['id'] 
        else: self.id = -1

        if('album_id' in input): self.album_id = input['album_id'] 
        else: self.album_id = -1

        if('width' in input): self.width = input['width'] 
        else: self.width = -1

        if('height' in input): self.height = input['height'] 
        else: self.height = -1

        self.sizes = []
        if('photo_75' in input):
            self.sizes.append( { 'name' : 75, 'url' : input['photo_75'] } )
        if('photo_130' in input):
            self.sizes.append( { 'name' : 103, 'url' : input['photo_130'] } )
        if('photo_604' in input):
            self.sizes.append( { 'name' : 604, 'url' : input['photo_604'] } )
        if('photo_807' in input):
            self.sizes.append( { 'name' : 807, 'url' : input['photo_807'] } )
        if('photo_1280' in input):
            self.sizes.append( { 'name' : 1280, 'url' : input['photo_1280'] } )        
        if('photo_2560' in input):
            self.sizes.append( { 'name' : 2560, 'url' : input['photo_2560'] } )

    def toDebugJSON(self):
        return {
            "type" : self.type,
            "id" : self.id,
            "album_id" : self.album_id,
            "width" : self.width,
            "height" : self.height,
            "sizes" : self.sizes  
        }