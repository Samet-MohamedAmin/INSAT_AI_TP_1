#! /bin/python3

import gi
gi.require_version('Gtk', '3.0')


from gi.repository import Gtk
import os.path


from test import Test

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.assistance_window = builder.get_object('assistance_window')
        self.input_goal = self.builder.get_object('input_goal')
        builder.get_object('file_chooser_faits').set_current_folder(os.path.curdir)
        builder.get_object('file_chooser_regles').set_current_folder(os.path.curdir)

    def get_current_page(self):
        current_page_index = self.assistance_window.get_current_page()
        current_page = self.assistance_window.get_nth_page(current_page_index)

        return current_page

    def set_current_page_complete(self, is_page_complete):
        self.assistance_window.set_page_complete(self.get_current_page(), is_page_complete)

    def file_set(self, widget):
        self.set_current_page_complete(True)

    def goal_check_toggled(self, widget):
        goal_active = widget.get_active()
        self.input_goal.set_text('')
        self.input_goal.set_can_focus(goal_active)
        self.input_goal.set_editable(goal_active)

        self.set_current_page_complete(not goal_active or self.input_goal.get_text())

    def input_goal_changed(self, widget):
        text = widget.get_text()

        if len(text) == 0:
            self.set_current_page_complete(False)
        else:
            self.set_current_page_complete(True)

    def on_prepare_page(self, window, widget):
        if self.builder.get_object('page_resume') == widget:
            self.file_faits = self.builder.get_object('file_chooser_faits').get_filename()
            self.file_regles = self.builder.get_object('file_chooser_regles').get_filename()

            goal = self.input_goal.get_text() or 'NOT ACTIVE'
            self.builder.get_object('resume_faits').set_text(os.path.basename(self.file_faits))
            self.builder.get_object('resume_regles').set_text(os.path.basename(self.file_regles))
            self.builder.get_object('resume_goal').set_text(goal)

    def cancel(self, *args):
        print('cancel')
        Gtk.main_quit()

    def quit(self, *args):
        test = Test(self.file_faits, self.file_regles, self.input_goal.get_text())
        msg = test.do_test()

        dialog = Gtk.MessageDialog(parent=self.assistance_window,
                                   flags=0,
                                   message_type=Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK,
                                   text='final result')
        dialog.format_secondary_text(msg)
        dialog.run()

        dialog.destroy()


        print('quit')
        Gtk.main_quit()


if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file('bla.glade')
    assistance_window = builder.get_object('assistance_window')

    handler = Handler(builder)
    builder.connect_signals(handler)


    assistance_window.show_all()

    Gtk.main()