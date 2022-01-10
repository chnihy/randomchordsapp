#! python3
# TODO Make it prettier
# TODO Chords need to be higher up, they're too low on screen


import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.button import Button
from kivy.uix.label import Label

from chords import randomchords, roots

import mingus.core.notes as notes
from mingus.containers import Note, NoteContainer
import mingus.core.chords as chords
from mingus.midi import fluidsynth


Window.maximize()

class Display(FloatLayout):
	pass

class Graphics(GridLayout):
	pass

class Controls(GridLayout):
	pass

class DifficultySettings(BoxLayout):
	pass

class MainLayout(Widget):
	def __init__(self, **kwargs):
		super(MainLayout, self).__init__(**kwargs)

		# Enter key functionality binding
		Window.bind(on_key_down = self._on_keyboard_down)
	
	
	# Objects from .kv
	graphics = ObjectProperty(None)
	chord_entry = ObjectProperty(None)
	difficulty_state = StringProperty('Easy')

	# Playing MIDI sounds via Mingus module
	def playchord(self, instance):
		fluidsynth.stop_everything()

		fluidsynth.init("./sounds/Grand Piano.sf2")

		chord = chords.from_shorthand(instance.text)

		nc = NoteContainer(chord)

		fluidsynth.play_NoteContainer(nc)

	# Difficulty Selection
	def set_difficulty(self, difficulty):
		self.difficulty_state = difficulty


	# When the user presses the GO button or ENTER
	def display_chord_buttons(self):
		
		# Exception classes
		class TooManyChords(Exception):
			pass
		
		# Num of chords - from <chord_id> text input
		if self.chord_entry.text == '':
			# If user enters no chords: 1 chord default 
			num_of_chords = 1 
		else:
			num_of_chords = int(self.chord_entry.text)
		


		try:
			# Clear out old buttons
			self.graphics.clear_widgets()
			
			# Max number of chords raises exception
			if num_of_chords > 12:
				raise TooManyChords
			
			# Generating our chordlist
			chordlist = randomchords(self.difficulty_state, num_of_chords)			

			# Create chord buttons
			for n in range(num_of_chords):

				chord_button = Button(text = chordlist[n],
							font_size = 20,
							size_hint = (None,None), 
							size= (120,120))
				
				# Making the button play it's chord
				chord_button.bind(on_press=self.playchord)

				self.graphics.add_widget(chord_button)
			
			# Set width of grid
			if num_of_chords < 4:
				self.graphics.width = num_of_chords * chord_button.width
			else:
				self.graphics.width = 4 * chord_button.width
			
			# Centering grid in display
			self.graphics.center = self.graphics.parent.center
			#self.graphics.pos_hint={'center_x': .5, 'center_y': .7}
		
		# Exceptions
		except TooManyChords:
				error_msg = Label(text = 'Error, too many chords', 
								size_hint=(None,None ), 
								font_size=30, 
								color=(0,0,0,1), 
								center=self.parent.center)
				self.graphics.width = error_msg.width
				self.graphics.add_widget(error_msg)
				self.graphics.center = self.graphics.parent.center

	# Enter key function
	def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
		if keycode == 40:
			self.display_chord_buttons()

class MainApp(App):
	
	def build(self):
		return MainLayout()

if __name__ == "__main__":
	MainApp().run()