import os
import sys
from urllib.parse import urlencode, parse_qsl

import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath


URL = sys.argv[0]
HANDLE = int(sys.argv[1])

ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
IMAGE_DIR = os.path.join(ADDON_PATH, 'resources', 'images')

# Public domain movies are from https://publicdomainmovie.net
# Here we use a hardcoded list of movies simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some website or online service.

def video_info():

    videos = [
                {
                    'genre': 'Drama',
                    'icon': os.path.join(IMAGE_DIR, 'icon.png'),
                    'fanart': os.path.join(IMAGE_DIR, 'fanart.jpg'),
                    'movies': [
                                {
                                    'title': 'The Stranger',
                                    'url': 'https://ia800908.us.archive.org/30/items/TheStranger_0/The_Stranger_512kb.mp4',
                                    'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Movie-Mystery-Magazine-July-1946.jpg',
                                    'plot': 'In 1946, Mr. Wilson (Edward G. Robinson) of the United Nations War Crimes Commission is hunting for '
                                            'a Nazism fugitive Franz Kindler (Orson Welles), a war criminal who has erased all evidence which '
                                            'might identify him. Kindler has assumed a new identity, Charles Rankin, '
                                            'and has become a University-preparatory school#United States and Canada teacher '
                                            'in a small town in the United States. ',
                                    'year': 1946,
                                },
                                {
                                    'title': 'The Iron Mask',
                                    'url': 'https://ia600702.us.archive.org/3/items/iron_mask/iron_mask_512kb.mp4',
                                    'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Ironmaskposter.jpg',
                                    'plot': 'The Iron Mask is a 1929 American part-talkie adventure film directed by Allan Dwan. '
                                              'It is an adaptation of the last section of the novel The Vicomte de Bragelonne by '
                                              'Alexandre Dumas, père, which is itself based on the French legend of The Man in the Iron Mask.',
                                    'year': 1929,
                                },
                                {
                                    'title': 'Meet John Doe',
                                    'url': 'https://ia804707.us.archive.org/30/items/meet_john_doe_ipod/video_512kb.mp4',
                                    'poster': 'https://publicdomainmovie.net/wikimedia.php?id=Poster_-_Meet_John_Doe_01.jpg',
                                    'plot': 'Meet John Doe is a 1941 in film United States comedy film drama film film directed and produced '
                                            'by Frank Capra, and starring Gary Cooper and Barbara Stanwyck. The film is about a "grassroots" '
                                            'political campaign created unwittingly by a newspaper columnist and pursued by a wealthy businessman.',
                                    'year': 1941,
                                },
                    ],
                },
               
            ]

    return videos


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    
    return '{}?{}'.format(URL, urlencode(kwargs))

   
def get_genres():
    """
    Get the list of video genres

    Here you can insert some code that retrieves
    the list of video sections (in this case movie genres) from some site or API.

    :return: The list of video genres
    :rtype: list
    """
    VIDEOS = video_info()
    
    return VIDEOS


def get_videos(genre_index):
    """
    Get the list of videofiles/streams.

    Here you can insert some code that retrieves
    the list of video streams in the given section from some site or API.

    :param genre_index: genre index
    :type genre_index: int
    :return: the list of videos in the category
    :rtype: list
    """

    VIDEOS = video_info()
    
    return VIDEOS[genre_index]

def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, 'Public Domain Movies')

    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')

    # Get movie genres
    genres = get_genres()

    # Iterate through genres
    for index, genre_info in enumerate(genres):


        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info['genre'])

        # Set images for the list item.
        list_item.setArt({'icon': genre_info['icon'], 'fanart': genre_info['fanart']})

        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre_info['genre'])
        info_tag.setGenres([genre_info['genre']])

        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)

        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True

        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)
   

def list_videos(genre_index):
    """
    Create the list of playable videos in the Kodi interface.

    :param genre_index: the index of genre in the list of movie genres
    :type genre_index: int
    """
    genre_info = get_videos(genre_index)

    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, genre_info['genre'])

    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')

    # Get the list of videos in the category.
    videos = genre_info['movies']

    # Iterate through videos.
    for video in videos:

        # Create a list item with a text label
        list_item = xbmcgui.ListItem(label=video['title'])

        # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
        # Here we use only poster for simplicity's sake.
        # In a real-life plugin you may need to set multiple image types.
        list_item.setArt({'poster': video['poster']})

        # Set additional info for the list item via InfoTag.
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setTitle(video['title'])
        info_tag.setGenres([genre_info['genre']])
        info_tag.setPlot(video['plot'])
        info_tag.setYear(video['year'])

        # Set 'IsPlayable' property to 'true'.
        # This is mandatory for playable items!
        list_item.setProperty('IsPlayable', 'true')

        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=play&video=https%3A%2F%2Fia600702.us.archive.org%2F3%2Fitems%2Firon_mask%2Firon_mask_512kb.mp4
        url = get_url(action='play', video=video['url'])

        #xbmc.log('list video'*10)
        #xbmc.log(str(url))
        #xbmc.log('list video'*10)

        #xbmc.log('url'*60)
        #xbmc.log(str(url))
        #xbmc.log('url'*60)

        # Add the list item to a virtual Kodi folder.
        # is_folder = False means that this item won't open any sub-list.
        is_folder = False

        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)

    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)

    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)
   

def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    # offscreen=True means that the list item is not meant for displaying,
    # only to pass info to the Kodi player
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(path)

    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)
   

def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """

    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
   
    # Check the parameters passed to the plugin
    if not params:

        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        list_genres()
   
    elif params['action'] == 'listing':

        # Display the list of videos in a provided category.
        list_videos(int(params['genre_index']))
   
    elif params['action'] == 'play':

        # Play a video from a provided URL.
        play_video(params['video'])
   
    else:

        # If the provided paramstring does not contain a supported action
        # we raise an exception. This helps to catch coding errors,
        # e.g. typos in action names.
        raise ValueError(f'Invalid paramstring: {paramstring}!')
       

if __name__ == '__main__':

    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])
    
