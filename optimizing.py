import windowing
import optimal as cvx
import optwindowing
import l0 as l0
import bilateral as bil
import totalVariation as tv
import wlsMultitone as wls


def main():

	debug = False


	filteringDict  = {0 : "cvx", 1 : "l0", 2: "bil", 3: "tv", 4: "wls"}
	moduleDict     = {"cvx" : cvx, "l0" : l0, "bil" : bil, "tv" : tv, "wls" : wls}
	

	#User defined parameters
	videoType      = 2
	procedure      = 3
	filteringType  = 0
		
	filesDictionary = {0 : {'videoFile'       : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1.mp4',
							'dosData'         : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy.txt',
					        'transformedFile' : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-transformed.txt', 
					        'optimizedFile'   : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/dos1-willy-optimized-' + filteringDict[filteringType]+'.txt', 
							'out_file'        : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/distorted-willy.avi', 
							'smoothVideo'     : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dos1/smooth-willy-' + filteringDict[filteringType]+'.avi', 
							'parameters-cvx'  : [800,200,300],
							'parameters-l0'   : [1e3, 1e5, 2.0],
							'parameters-bil'  : [50,400,800],
							'parameters-tv'   : [800],},
					   1 : {'videoFile'       : '/home/abhishek/Desktop/Main/Others/BTP/tracks/1.mp4',
							'dosData'         : '/home/abhishek/Desktop/Main/Others/BTP/tracks/danceraw1.txt',
							'transformedFile' : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-transformed1.txt',
							'optimizedFile'   : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-optimized1-' + filteringDict[filteringType]+'.txt',
							'out_file'        : '/home/abhishek/Desktop/Main/Others/BTP/tracks/distorted-dance1.avi',
							'smoothVideo'     : '/home/abhishek/Desktop/Main/Others/BTP/tracks/smooth-dance1-' + filteringDict[filteringType]+'.avi',
							'parameters-cvx'  : [800,200,300],
							'parameters-l0'   : [1e3, 1e5, 2.0],
							'parameters-bil'  : [30,100,100],
							'parameters-tv'   : [800],},
					   2 : {'videoFile'       : '/home/abhishek/Desktop/Main/Others/BTP/tracks/1.mp4',
							'dosData'         : '/home/abhishek/Desktop/Main/Others/BTP/tracks/danceraw2.txt',
							'transformedFile' : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-transformed2.txt',
							'optimizedFile'   : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-optimized2-' + filteringDict[filteringType]+'.txt',
							'out_file'        : '/home/abhishek/Desktop/Main/Others/BTP/tracks/distorted-dance2.avi',
							'smoothVideo'     : '/home/abhishek/Desktop/Main/Others/BTP/tracks/smooth-dance2-' + filteringDict[filteringType]+'.avi',
							'parameters-cvx'  : [500,200,300],
							'parameters-l0'   : [1e3, 1e5, 2.0],
							'parameters-bil'  : [50,400,800],
							'parameters-tv'   : [800],},
					   3 : {'videoFile'       : '/home/abhishek/Desktop/Main/Others/BTP/tracks/1.mp4',
							'dosData'         : '/home/abhishek/Desktop/Main/Others/BTP/tracks/danceraw3.txt',
							'transformedFile' : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-transformed3.txt',
							'optimizedFile'   : '/home/abhishek/Desktop/Main/Others/BTP/tracks/dance-optimized3' + filteringDict[filteringType]+'.txt',
							'out_file'        : '/home/abhishek/Desktop/Main/Others/BTP/tracks/distorted-dance3.avi',
							'smoothVideo'     : '/home/abhishek/Desktop/Main/Others/BTP/tracks/smooth-dance3-' + filteringDict[filteringType]+'.avi',
							'parameters-cvx'  : [800,200,300],
							'parameters-l0'   : [1e3, 1e5, 2.0],
							'parameters-bil'  : [50,400,800],
							'parameters-tv'   : [800],},							 								
					}

	method = moduleDict[filteringDict[filteringType]]

	if procedure==1:
		windowing.PlayAndGetData(filesDictionary[videoType]['videoFile'], filesDictionary[videoType]['dosData'], 
							 filesDictionary[videoType]['transformedFile'], filesDictionary[videoType]['out_file'], 
							 debug, videoType, True)
	
	elif procedure==2:
		method.optimizeData(filesDictionary[videoType]['transformedFile'], filesDictionary[videoType]['optimizedFile'], 
						  filesDictionary[videoType]['parameters-'+filteringDict[filteringType]], debug)
	
	else:
		optwindowing.displayOptimizedData(filesDictionary[videoType]['videoFile'], filesDictionary[videoType]['optimizedFile'],
	                                    filesDictionary[videoType]['smoothVideo'], debug, videoType, True)


if __name__ == "__main__":
	main()