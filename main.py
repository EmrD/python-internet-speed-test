import customtkinter as ctk
import speedtest  #type:ignore
import threading
import time


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("Internet Speed Test")
app.geometry("400x400")
app.resizable(False, False)


loading = False


def loading_animation():
    dots = ""
    while loading:
        dots = "." if dots == "..." else dots + "."
        status_label.configure(text=f"Testing, please wait{dots}")
        time.sleep(0.5)


def show_loading():
    global loading
    loading = True
    download_label.configure(text="Download Speed: - Mbps", fg_color="transparent")
    upload_label.configure(text="Upload Speed: - Mbps", fg_color="transparent")
    ping_label.configure(text="Ping: - ms", fg_color="transparent")
    server_label.configure(text="Server: - ")
    test_button.configure(state="disabled")
    
    
    threading.Thread(target=loading_animation, daemon=True).start()


def set_label_color(label, value, thresholds):
    if value >= thresholds['high']:
        label.configure(fg_color="green")
    elif value >= thresholds['medium']:
        label.configure(fg_color="orange")
    else:
        label.configure(fg_color="red")


def run_speed_test():
    show_loading()
    thread = threading.Thread(target=speed_test)
    thread.start()


def speed_test():
    global loading
    try:
        speed = speedtest.Speedtest()
        speed.get_best_server()
        server = speed.results.server['host']
        
        download_speed = speed.download() / 1_000_000  
        upload_speed = speed.upload() / 1_000_000      
        ping = speed.results.ping                      

        
        download_label.configure(text=f"Download Speed: {download_speed:.2f} Mbps")
        upload_label.configure(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        ping_label.configure(text=f"Ping: {ping:.2f} ms")
        server_label.configure(text=f"Server: {server}")
        status_label.configure(text="Test Completed!")
        test_button.configure(state="normal")

        
        set_label_color(download_label, download_speed, {'high': 50, 'medium': 20})
        set_label_color(upload_label, upload_speed, {'high': 10, 'medium': 5})
        set_label_color(ping_label, ping, {'high': 50, 'medium': 100})
        
    except Exception as e:
        status_label.configure(text=f"Error: {str(e)}")
    finally:
        loading = False
        test_button.configure(state="normal")


title_label = ctk.CTkLabel(app, text="Internet Speed Test", font=("Arial", 24))
title_label.pack(pady=15)


test_button = ctk.CTkButton(app, text="Run Speed Test", command=run_speed_test, width=150, height=40)
test_button.pack(pady=10)


status_label = ctk.CTkLabel(app, text="", font=("Arial", 14))
status_label.pack(pady=10)


result_frame = ctk.CTkFrame(app)
result_frame.pack(pady=20, fill="both", expand=True)


download_label = ctk.CTkLabel(result_frame, text="Download Speed: - Mbps", font=("Arial", 16))
download_label.pack(pady=5)

upload_label = ctk.CTkLabel(result_frame, text="Upload Speed: - Mbps", font=("Arial", 16))
upload_label.pack(pady=5)

ping_label = ctk.CTkLabel(result_frame, text="Ping: - ms", font=("Arial", 16))
ping_label.pack(pady=5)

server_label = ctk.CTkLabel(result_frame, text="Server: - ", font=("Arial", 16))
server_label.pack(pady=5)


app.mainloop()
