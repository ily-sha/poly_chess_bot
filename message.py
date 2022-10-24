update_id = ''


class Message:
    def __init__(self, message_json):
        print(message_json)
        self.__message_json = message_json
        if "message" in message_json:
            self.__message_type = "message"
            self.__message = message_json["message"]
            self.__chat_id = self.__message["from"]["id"]
            self.__username = self.__message["from"]["username"]
            self.__text_message = False
            self.__location_message = False
            self.__has_venue_param = False
            self.__forward_message = False
            self.__document_message = False
            self.__live_period = False

            self.__text = None
            self.__location = None
            self.__file_id = None
            self.__file_name = None

            if "text" in self.__message:
                self.__text_message = True
                self.__text = self.__message["text"]
            if "location" in self.__message:
                self.__location_message = True
                self.__location = self.__message["location"]
                if "live_period" in self.__message["location"]:
                    self.__live_period = True
            if "venue" in self.__message:
                self.__has_venue_param = True
            if "forward_from" in self.__message:
                self.__forward_message = True
            if "document" in self.__message:
                self.__document_message = True
                self.__file_name = self.__message["document"]["file_name"]
                self.__file_id = self.__message["document"]["file_id"]
        else:
            self.__message_type = "else"

    def get_chat_id(self):
        return self.__chat_id

    def get_username(self):
        return self.__username

    def is_text_message(self):
        return self.__text_message

    def get_text(self):
        return self.__text

    def is_location_message(self):
        return self.__location_message

    def get_location(self):
        return self.__location

    def has_venue(self):
        return self.__has_venue_param

    def is_forward_message(self):
        return self.__forward_message

    def is_document_message(self):
        return self.__document_message

    def get_file_name(self):
        return self.__file_name

    def get_file_type(self):
        return self.__file_name.split(".")[1]

    def get_file_id(self):
        return self.__file_id

    def is_live_location(self):
        return self.__live_period

    def get_message_type(self):
        return self.__message_type
