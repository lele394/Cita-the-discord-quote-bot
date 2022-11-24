import gspread
from oauth2client.service_account import ServiceAccountCredentials



scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)






def GetBookmarksOfUser(userID):#marche
    """return either a list of bookmarks or [False] if user doesn't exist or user cleared bookmarks"""
    client = gspread.authorize(creds)
    sheet = client.open('bookmark').sheet1

    users = sheet.col_values(1)
    if "@"+str(userID) in users: #col 1 = users
        UserIndex = users.index("@"+str(userID)) + 1
        bookmarks = sheet.cell(UserIndex, 2).value.split(" ")
        try:
            bookmarks.remove("")
        except ValueError:
            bookmarks=bookmarks

        if bookmarks != []:
            return bookmarks #return user bookmarks
        else:
            return [False]
    else:
        return [False]




def AddBookmarkToUser(userID, bookmark):
    """add user if user doesn't exists and add bookmarks"""
    client = gspread.authorize(creds)
    sheet = client.open('bookmark').sheet1
    if GetBookmarksOfUser(userID)[0] == False:
        sheet.insert_row(["@"+str(userID), bookmark], 1)

    else:
        UserIndex = sheet.col_values(1).index("@"+str(userID)) + 1

        book = " ".join(GetBookmarksOfUser(userID)) + " " + bookmark
        sheet.update_cell(UserIndex, 2, book)




def DeleteBookmarkOfUser(userID, bookmark):
    """add user if user doesn't exists and add bookmarks"""

    client = gspread.authorize(creds)
    sheet = client.open('bookmark').sheet1
    if GetBookmarksOfUser(userID)[0] == False:
        return

    else:
        UserIndex = sheet.col_values(1).index("@"+str(userID)) + 1
        bookmarks = GetBookmarksOfUser(userID)
        bookmarks.remove(bookmark)
        book = " ".join(bookmarks)
        sheet.update_cell(UserIndex, 2, book)




def ResetBookmarksOfUser(userID):
    """add user if user doesn't exists and add bookmarks"""
    client = gspread.authorize(creds)
    sheet = client.open('bookmark').sheet1
    if GetBookmarksOfUser(userID)[0] == False:
        return "You don't have any bookmarks to clear."

    else:
        UserIndex = sheet.col_values(1).index("@"+str(userID)) + 1
        sheet.update_cell(UserIndex, 2, "")
        return "Bookmarks cleared!"


























#
