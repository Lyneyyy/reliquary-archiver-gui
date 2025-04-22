print("[!] Log window, this window can be minimized")

import dearpygui.dearpygui as dpg
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def create_sep():
    dpg.add_spacer(height=10)
    dpg.add_separator()
    dpg.add_spacer(height=10)

def npcap_install():
    dpg.configure_item("wlc", show=False)
    
    check_npcap()
    
def npcap_download():
    os.system("start curl -o npcap-1.81.exe https://npcap.com/dist/npcap-1.81.exe && npcap-1.81.exe")

def check_npcap():
    if os.path.isfile(r"C:\Windows\System32\Npcap\wpcap.dll") == False:
        dpg.configure_item("npcap", show=True)
    else:
        check_rel()

def check_rel():
    if os.path.isfile(r"reliquary-archiver_x64.exe") == False:
        dpg.configure_item("dl_ra", show=True)
    else:
        dpg.set_viewport_width(600) 
        dpg.set_viewport_height(550) 
        dpg.configure_item("dl_ra", show=False)   
        dpg.configure_item("npcap", show=False)     
        dpg.configure_item("main_ui", show=True)    
        
def download_ra():
    os.system("start powershell curl -o reliquary-archiver_x64.exe https://github.com/IceDynamix/reliquary-archiver/releases/download/v0.4.0/reliquary-archiver_x64.exe")

def open_hsr():
    if os.path.isfile(r"C:\Program Files\HoYoPlay\launcher.exe") == False:
        dpg.configure_item("warning_game", show=True)
    else:
        os.system(rf""" "C:\Program Files\HoYoPlay\launcher.exe" --game=hkrpg_global """)

def open_archive():
    path = os.listdir()

    for x in path:
        if "archive_output" in x:
            os.system(f"explorer /select,\"{x}\"")
            return
            break
        
    dpg.configure_item("warning_file", show=True)
    return


dpg.create_context()
with dpg.window(tag="Primary Window"):
    
    with dpg.group(tag="wlc"):
        dpg.add_text("Reliquary Archiver GUI")
        dpg.add_text("""A tool to create a relic export from network packets of a certain turn-based anime game. \n\nThis setup will prepare your system to run Reliquary Archiver, it will firstly verify if npcap is installed, if not it will install it.""", wrap=550)
        
        # Spacer to push content down
        create_sep()

        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Quit", callback=dpg.destroy_context)
            dpg.add_button(label="Continue >", callback=npcap_install)

    with dpg.group(tag="npcap", show=False):
        dpg.add_text("Reliquary Archiver GUI")
        dpg.add_text("""Npcap is NOT installed on this system. Please download and install it.\n\n- [!] *IF* you USE WIFI, "enable Support raw 802.11 traffic (and monitor mode) for wireless adapters"\n- *Check* winpcap "api-compatible mode" """, wrap=550)
        
        # Spacer to push content down
        create_sep()

        
        with dpg.group(horizontal=True):
            dpg.add_button(label="Quit", callback=dpg.destroy_context)
            dpg.add_button(label="Download and start setup >", callback=npcap_download)
            dpg.add_button(label="Next >", callback=check_npcap)
        
        dpg.add_text("*The setup window will be minimzed by default")

    with dpg.group(tag="dl_ra", show=False):
        dpg.add_text("Reliquary Archiver GUI")
        dpg.add_text("The system is ready to use reliquary archiver, it will now download it", wrap=550)
        create_sep()     
        with dpg.group(horizontal=True):
            dpg.add_button(label="Quit", callback=dpg.destroy_context)
            dpg.add_button(label="Download >", callback=download_ra)
            dpg.add_button(label="Next >", callback=check_rel)

    with dpg.group(tag="main_ui", show=False):
        width, height, channels, data = dpg.load_image(resource_path("hsr_hyperdrive.jpg"))
        
        with dpg.texture_registry(show=False):
            dpg.add_static_texture(width=width, height=height, default_value=data, tag="texture_tag")


        dpg.add_text("Reliquary Archiver GUI")
        dpg.add_text("- 1. Open the game and wait on the \"Click to start\" screen\n- 2. Run reliquary-archiver and then start the game \n- 3. When the tool says to press enter to exit press it, it will create a \"archive_output_*.json\" file in directory of this program\n\n*Screen to wait", wrap=550)
        dpg.add_image("texture_tag")
        
        create_sep()     
        
        with dpg.group(horizontal=True):
            dpg.add_button(label="1. Open HSR", callback=open_hsr, height=40, tag="btn_hsr")
            dpg.add_button(label="2. Start reliquary-archiver", callback=lambda: os.system("start reliquary-archiver_x64.exe"), height=40)
            dpg.add_button(label="3. View archive file", callback=open_archive, height=40, tag="view_file")

    
    
    # The popup is now attached to the window rather than the text
    with dpg.popup(parent="view_file", modal=True, tag="warning_file"):
        dpg.add_text("archiver_output.json not found, please run reliquary-archiver before.")
        dpg.add_button(label="Close", callback=lambda: dpg.configure_item("warning_file", show=False))

    with dpg.popup(parent="btn_hsr", modal=True, tag="warning_game"):
        dpg.add_text("HSR (Hoyoplay) not found, please manually run the game.")
        dpg.add_button(label="Close", callback=lambda: dpg.configure_item("warning_game", show=False))

dpg.create_viewport(title='Reliquary Archiver GUI', width=600, height=200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()