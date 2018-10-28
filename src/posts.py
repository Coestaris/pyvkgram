class post:
    
    def escapeText(self):
        return self.text.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("]", "\\]").replace("`", "\\`")

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

        if('attachments' in input and len(input['attachments']) != 0):
            for attachment in input['attachments']:
                if(attachment['type'] == 'photo' or attachment['type'] == 'posted_photo'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'link'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'doc'):
                    print('Unknown format {}'.format(attachment['type']))
                elif(attachment['type'] == 'video'):
                    print('Unknown format {}'.format(attachment['type']))
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
            "text" : (self.text[1:50] if len(self.text) > 50 else self.text) if self.text != '' else "<empty>",
            "attachments" : [],
            "likeCount" : self.likeCount,
            "repostsCount" : self.repostsCount,
            "commentsCount" : self.commentsCount  
        }