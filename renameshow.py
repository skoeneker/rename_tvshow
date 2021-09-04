# File_move.py
# Written by: Steven Koeneker
# Project started: 18 Aug 2020
# Purpose: Move tv episodes that have been ripped by HandBrakeCLI to final directory
# Purpose2: Practice Python

# Start

# Function: exit on error
# Function Input: error reason
# Exit with notice if there is a problem with the files that were ripped
# Exit with different notice for feature not yet implemented
def exit_error(reason):
    if reason == 1:
        print("The number of files ripped was not what was expected")
    else:
        print("That feature is not yet enabled")
    exit()

# Function: Change the Series
# Function Input: None
# Ask the name of the new series
def change_series():
    correct = 'f'
    while correct == 'f':
        series = input('What is the new series name? ')
        print('The new series name is:', series)
        correct = input('Is this correct?(t/f)')
    
# Ask if starting from the beginning of the series
    season = 1
    new_series = 't'
    new_series = input('Are you starting at Season 1? (t/f) ')
# Ask How many Seasons
    num_seasons = 1
    num_seasons = input('How many Seasons are there?')
    
    episode = 0
     
# If new series
#   Write to data file: Series, Season 01, Episode 0
#   Make new directories in Plex/tv-shows
# Else
#   Ask what Season and what Episode to start
#   Write to data file: Series, Season, Episode
# Endif
# Return Series, Season, Episode
    if new_series == 't':
        tvshowfile = open("tv_show_tracker.txt", "w")
        tvshowfile.write('%s\n' % series)
        tvshowfile.write('%s\n' % str(season))
        tvshowfile.write('%s\n' % str(episode))
        tvshowfile.close()
        path_base = 'files'
        path_base2 = 'plex'
        path_base3 = 'tv-shows'
        i = 1
        os.mkdir(os.path.join('/', path_base, path_base2, path_base3, series))
        while i <= int(num_seasons):
            if i <= 9:
                path_season = 'Season 0' + str(i)
            else:
                path_season = 'Season ' + str(i)
            new_directory = os.path.join('/', path_base, path_base2, path_base3, series, path_season)
            os.mkdir(new_directory)
            i = i + 1
    else:
        season = input("What Season are you starting with? ")
        episode = input("What episode are you starting with? ")
        tvshowfile = open("tv_show_tracker.txt", "w")
        tvshowfile.write('%s\n' % series)
        tvshowfile.write('%s\n' % str(season))
        tvshowfile.write('%s\n' % str(episode))
        tvshowfile.close()
    return series, str(season), str(episode)


# Function: Change Season
# Function Input: Series, old season
def change_season(series, season):
    #error_reason = 2
    #exit_error(error_reason)

# Display the current series and the old season
    print('The current series is: ', series, ' and the old season is: ', season)
    
# Ask for the new season
    new_season = input('What is the new season (do not use leading zeros): ')
# Ask if starting from the first episode
    correct = 't'
    correct = input('Is this season starting with the first episode? (t/f) ')
# If first episode
#   Write to data file: Series, Season, Episode 0
# Else
#   Ask what episode to start
# Endif
    if correct == 't':
        episode = '0'
        tvshowfile = open("tv_show_tracker.txt", "w")
        tvshowfile.write('%s\n' % series)
        tvshowfile.write('%s\n' % str(new_season))
        tvshowfile.write('%s\n' % str(episode))
        tvshowfile.close()
    else:
        episode = input('What episode was the last recorded?')
        tvshowfile = open("tv_show_tracker.txt", "w")
        tvshowfile.write('%s\n' % series)
        tvshowfile.write('%s\n' % str(new_season))
        tvshowfile.write('%s\n' % str(episode))
        tvshowfile.close()
    
# Return Series, Season, Episode
    return series, new_season, episode

# Function:  Manual Map
# Function Input: Series, Season, Episode, # episode
# Write the series, season, episode and # episode
# What is the correct mapping per episode
# Create list of episode numbers as strings - episodes must be 2 digit
# Return list of episode numbers


def manual_map(series, season, num_episode):
    print('The Series : ' + series)
    print('The Season is:' + season)
    print('There are ' + num_episode + ' episodes.')
    episode_counter = 0
    episode_list = list()
    position_list = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    while episode_counter < str(num_episode):
        next_episode = input("What is the episode number for the " + position_list(episode_counter) + "ripped file?")
        if len(next_episode) < 2:
            episode_list.append('0' + next_episode)
        else:
            episode_list.append(next_episode)
        episode_counter = episode_counter + 1
    return episode_list


# Main
# Read file with current series, season and episode and remove end of line marker
import fnmatch, os
data = open("tv_show_tracker.txt", "r")
a = data.readline()
series = a.replace('\n', '')
b = data.readline()
season = b.replace('\n', '')
c = data.readline()
episode = c.replace('\n', '')
data.close()
# Ask if correct series
correct = 't'
correct = input('Is ' + series + ' the correct series?(t/f)')
if correct != 't':
    series, season, episode = change_series()

# If not correct series; go to function Change Series
# Ask if correct season
correct = 't'
correct = input('Is ' + season + ' the correct season?(t/f)')
# If not correct season; go to function Change Season
if correct != 't':
    series, season, episode = change_season(series, season)

# Write Series, Season, episode
print('The Series is:', series, '\n', 'The Season is:', season, '\n', 'The last episode moved was:', episode, '\n')

# Ask how many episodes to rename
num_episodes = input('How many episodes are being moved? ')
num_episodes_int = int(num_episodes)
# Check to see how many episodes have been ripped
cwd = os.getcwd()
num_ripped = len(fnmatch.filter(os.listdir(cwd), '*.mkv'))

# if # to rename not equal to # ripped; error message and quit
if (num_episodes_int != num_ripped):
    error_reason = 1
    exit_error(error_reason)

# create a list of file names
#    Set the file paths
#    check to see if ripped files are in order
path_base_1 = 'files'
path_base_2 = 'plex'
path_base_3 = 'tv-shows'
path_series = series
if int(season) <= 9:
    path_season = 'Season 0' + season
else:
    path_season = 'Season ' + season
ripped_files = sorted(fnmatch.filter(os.listdir(cwd), '*.mkv'))
new_file_name = list()

# Ask if episodes are in order (i.e. air date = disc order)
correct = 't'
correct = input('Are the episodes in the correct order? (t/f)')

# If not in order
#   Go to function Manual Mapping
# Else if
#   Create list of file names

if correct != 't':
    out_of_order_episode_list = list()
    out_of_order_episode_list = manual_map(series, season, num_episodes)
    episode_counter = 0
    for ripped_files in ripped_files:
        if int(season) <= 9:
            new_name = series + ' s0' + season + 'e' + out_of_order_episode_list(episode_counter) + '.mkv'
        else:
            new_name = series + ' s' + season + 'e' + out_of_order_episode_list(episode_counter) + '.mkv'
        new_file_name.append(os.path.join('/', path_base_1, path_base_2, path_base_3, path_series, path_season, new_name))
        episode_counter = episode_counter +1
else:
    for ripped_file in ripped_files:
        episode = int(episode) + 1
        if int(season) <= 9:
            if int(episode) <= 9:
                new_name = series + ' s0' + season + "e0" + str(episode) + '.mkv'
            else:
                new_name = series + ' s0' + season + 'e' + str(episode) + '.mkv'
        else:
            if int(episode) <= 9:
                new_name = series + ' s' + season + "e0" + str(episode) + '.mkv'
            else:
                new_name = series + ' s' + season + 'e' + str(episode) + '.mkv'
        new_file_name.append(os.path.join('/', path_base_1, path_base_2, path_base_3, path_series, path_season, new_name))


# Copy episodes to final location
i = 0
for ripped_file in ripped_files:
    os.rename(ripped_file, new_file_name[i])
    i = i + 1
              

# Write Series, Season, episode to file
data = open("tv_show_tracker.txt", "w")
data.write('%s\n' % series)
data.write('%s\n' % season)
data.write('%s\n' % episode)
data.close()
# Write completion message
print('Renaming program is complete')
# End
