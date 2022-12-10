class Message:
    def __init__(self, message_json):

        self.__message_type = None
        self.__live_period = None
        self.__text = None
        self.__location = None
        self.__file_id = None
        self.__file_name = None
        self.__username = None
        self.__edit_date = None
        self.__chat_id = None

        self.__location_message = False
        self.__live_message = False

        self.__message_json = message_json
        if "message" in message_json:
            self.__message_type = "message"
            self.__message = message_json["message"]
            self.__chat_id = self.__message["from"]["id"]

            self.__date = message_json["message"]["date"]
            if "username" in self.__message["from"]:
                self.__username = self.__message["from"]["username"]
            self.__text_message = False
            self.__has_venue_param = False
            self.__forward_message = False
            self.__document_message = False
            if "text" in self.__message:
                self.__text_message = True
                self.__text = self.__message["text"]
            if "location" in self.__message:
                self.__location_message = True
                self.__location = self.__message["location"]
                if "live_period" in self.__message["location"]:
                    self.__live_message = True
                    self.__live_period = self.__location["live_period"]
            if "venue" in self.__message:
                self.__has_venue_param = True
            if "forward_from" in self.__message:
                self.__forward_message = True
            if "document" in self.__message:
                self.__document_message = True
                self.__file_name = self.__message["document"]["file_name"]
                self.__file_id = self.__message["document"]["file_id"]
        elif "edited_message" in message_json:
            self.__message_type = "edited_message"
            self.__chat_id = message_json["edited_message"]["from"]["id"]
            if "location" in message_json["edited_message"]:
                self.__location_message = True
                if "horizontal_accuracy" in message_json["edited_message"]["location"] or \
                        "heading" in message_json["edited_message"]["location"] or \
                        "live_period" in message_json["edited_message"]["location"]:
                    self.__live_message = True
                    if "location" in message_json["edited_message"]:
                        self.__location = message_json["edited_message"]["location"]
            if "edit_date" in message_json["edited_message"]:
                self.__edit_date = message_json["edited_message"]["edit_date"]
        else:
            self.__message_type = "else"

    def get_edit_date(self):
        return self.__edit_date

    def get_chat_id(self):
        return self.__chat_id

    def get_username(self):
        return self.__username

    def is_text_message(self):
        return self.__text_message

    def get_text(self):
        return self.__text

    def get_date(self):
        return self.__date

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
        return self.__live_message

    def get_message_type(self):
        return self.__message_type

    def get_live_period(self):
        return self.__live_period

