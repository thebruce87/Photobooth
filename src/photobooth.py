import configparser, picamera, pygame, shutil, subprocess, time

# Local libraries
import button, display, pngview
from aspect_scale import aspect_scale

config = configparser.ConfigParser()
config.read('photobooth.ini')

button.init()

display = display.Display(int(config['Display']['width']),
                          int(config['Display']['height']))

buttons = {
	'green': button.Button(int(config['Buttons']['green'])),
	'red': button.Button(int(config['Buttons']['red']))
}

pngImages = {
	'foto': pngview.PNGView('images/foto.png'),
	'smile': pngview.PNGView('images/smile.png'),
	'timer_1': pngview.PNGView('images/timer_1.png'),
	'timer_2': pngview.PNGView('images/timer_2.png'),
	'timer_3': pngview.PNGView('images/timer_3.png'),
	'wait': pngview.PNGView('images/wait.png')
}

pygameImages = {
	'ok': pygame.image.load('images/ok.png')
}

sleep = float(config['Misc']['countdownSleep'])

flags = {
	'run': True,
	'capture': False
}

captureName = 'capture.jpg'

previewCamera = picamera.PiCamera()
previewCamera.vflip = config['Misc']['previewFlip']


## ----- Functions -------------------------------------------------------------

def setupPygame():
	pygame.init()
	pygame.mouse.set_visible(0)
	pygame.display.set_mode((display.width, display.height))

def setupPreviewCamera():
	previewCamera = picamera.PiCamera()
	previewCamera.vflip = config['Misc']['previewFlip']

def takeAPicture():
	captureProcess = subprocess.Popen(['gphoto2', '--capture-image-and-download',
	                                  'filename=' + captureName])
	captureProcess.wait()

def disablePreview():
	previewCamera.stop_preview()

def enablePreview():
	previewCamera.start_preview()

def savePhoto():
	safeTime = str(time.time())
	shutil.move(captureName, config['Paths']['output'] + '/'
		+ config['Misc']['imagePrefix'] + safeTime + '.jpg')

def waitUntil(condition):
	while not condition:
		pass

def buttonPressed(gpio):
	pass

## ----- Setup -----------------------------------------------------------------

#button.init()

setupPygame()
#setupPreviewCamera()

enablePreview()

pngImages['foto'].show()


## ----- Infinite loop ---------------------------------------------------------

while flags['run']:
	#flags['run'] = False

	if buttons['red'].isPressed():
		flags['capture'] = True
		pngImages['foto'].terminate()

	if flags['capture']:
		flags['capture'] = False

		pngImages['timer_3'].show()
		time.sleep(sleep)
		pngImages['timer_3'].terminate()

		pngImages['timer_2'].show()
		time.sleep(sleep)
		pngImages['timer_2'].terminate()

		pngImages['timer_1'].show()
		time.sleep(sleep)
		pngImages['timer_1'].terminate()

		pngImages['smile'].show()
		
		takeAPicture()

		pngImages['smile'].terminate()

		pngImages['wait'].show()

		image = pygame.image.load("capt0000.jpg")
		scaledImage = pygame.transform.aspect_scale(image, (screenHeight,
		                                            screenHeight))
		
		screen.blit(scaledImage, (0, 0))

		screen.blit(pygameImages['ok'], (0, 0))
		pygame.display.update()

		disablePreview()
		pngImages['wait'].terminate()

		waitUntil(buttons['green'].isPressed())

		savePhoto()

		screen.fill((0, 0, 0))
		pygame.display.update()

		enablePreview()

		pngImages['foto'].show()