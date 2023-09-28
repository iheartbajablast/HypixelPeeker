import tkinter as tk
from tkinter import ttk
import requests
import json
import customtkinter
from ttkthemes import themed_tk as thk
import re
import sys
from tkinter import *
from ctypes import windll
import pywinstyles
from tkinter import Listbox
from tkinter import ttk, PhotoImage
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import Listbox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# Set appearance mode and color theme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

api_key = "00a3e5af-7e93-4253-a2fd-6dac18e17f62"




def show_item_details(event):
    selected_item = auctions_tree.selection()
    if selected_item:
        item_data = auctions_tree.item(selected_item, "values")
        item_name = item_data[0]
        lore = item_data[1]
        starting_bid = item_data[2]
        highest_bid = item_data[3]

        # Create a new window to display item details
        details_window = customtkinter.CTkToplevel(root)
        details_window.attributes("-topmost", True)
        details_window.title("Item Details")
        pywinstyles.apply_style(details_window, "aero")

        # Add labels to display item details
        item_name_label = customtkinter.CTkLabel(details_window, text=f"Item Name: {item_name}")
        item_name_label.pack()

        lore_label = customtkinter.CTkLabel(details_window, text=f"Lore: {lore}")
        lore_label.pack()

        starting_bid_label = customtkinter.CTkLabel(details_window, text=f"Starting Bid: {starting_bid}")
        starting_bid_label.pack()

        highest_bid_label = customtkinter.CTkLabel(details_window, text=f"Highest Bid: {highest_bid}")
        highest_bid_label.pack()


recently_viewed_players = []


# Function to fetch player UUID from Mojang API
def get_uuid():
    username = username_entry.get()
    mojang_api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"

    response = requests.get(mojang_api_url)

    if response.status_code == 200:
        player_data = response.json()
        player_uuid = player_data["id"]
        fetch_hypixel_data(player_uuid)

        # Add the username to the recently viewed list
        recently_viewed_players.append(username)

        # Limit the list to the last N viewed players (e.g., 10)
        max_recent_players = 10
        if len(recently_viewed_players) > max_recent_players:
            recently_viewed_players.pop(0)

    else:
        output_tree.delete(*output_tree.get_children())
        output_tree.insert("", "end", text="Error", values=("Player not found",))



def fetch_hypixel_data(player_uuid):
    global skyblock_data
    hypixel_api_url = f"https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={player_uuid}"  # Replace with your Hypixel API key
    print("https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={player_uuid}")

    response = requests.get(hypixel_api_url)

    if response.status_code == 200:
        skyblock_data = response.json()
        display_data_in_treeview(skyblock_data)
        cute_name(skyblock_data)
        return skyblock_data
    else:
        output_tree.delete(*output_tree.get_children())
        output_tree.insert("", "end", text="Error", values=("Hypixel data not found",))

def cute_name(skyblock_data):
    global profile_0
    global profile_1
    global profile_2
    global profile_3
    global profile_4
    global profile_5
    try:
        profile_0 = skyblock_data.get("profiles", [])[0].get("cute_name")
        if profile_0:
            print("Cute Name:", profile_0)
    except:
        profile_0 = ""

    try:
        profile_1 = skyblock_data.get("profiles", [])[1].get("cute_name")
        if profile_1:
            print("Cute Name:", profile_1)
    except:
        profile_1 = ""

    try:
        profile_2 = skyblock_data.get("profiles", [])[2].get("cute_name")
        if profile_2:
            print("Cute Name:", profile_2)
    except:
        profile_2 = ""

    try:
        profile_3 = skyblock_data.get("profiles", [])[3].get("cute_name")
        if profile_3:
            print("Cute Name:", profile_3)
    except:
        profile_3 = ""

    try:
        profile_4 = skyblock_data.get("profiles", [])[4].get("cute_name")
        if profile_4:
            print("Cute Name:", profile_4)
    except:
        profile_4 = ""

    try:
        profile_5 = skyblock_data.get("profiles", [])[5].get("cute_name")
        if profile_5:
            print("Cute Name:", profile_5)
    except:
        profile_5 = ""
    
    profile_tabs(profile_0, profile_1, profile_2, profile_3, profile_4, profile_5, skyblock_data)
    
balance_labels = {}
showgraph = {}

def format_balance(balance):
    # Check if balance is a valid number
    try:
        balance = float(balance)
    except (ValueError, TypeError):
        return ""

    # Round to the nearest hundredth and add commas
    formatted_balance = "{:,.2f}".format(balance)
    return formatted_balance

def data_per_tab(skyblock_data, profile_0, profile_1, profile_2, profile_3, profile_4, profile_5, selected_profile):
    # Initialize balance variables with default values
    balance_0 = ""
    balance_1 = ""
    balance_2 = ""
    balance_3 = ""
    balance_4 = ""
    balance_5 = ""
    
    try:
        banking_data = skyblock_data.get("profiles", [])
        balance_0 = format_balance(banking_data[0].get("banking", {}).get("balance"))
        balance_1 = format_balance(banking_data[1].get("banking", {}).get("balance"))
        balance_2 = format_balance(banking_data[2].get("banking", {}).get("balance"))
        balance_3 = format_balance(banking_data[3].get("banking", {}).get("balance"))
        balance_4 = format_balance(banking_data[4].get("banking", {}).get("balance"))
        balance_5 = format_balance(banking_data[5].get("banking", {}).get("balance"))
    except:
        print("")
    if balance_0 == "":
        balance_0 = "Bank API Disabled"
    if balance_1 == "":
        balance_1 = "Bank API Disabled"
    if balance_2 == "":
        balance_2 = "Bank API Disabled"
    if balance_3 == "":
        balance_3 = "Bank API Disabled"
    if balance_4 == "":
        balance_4 = "Bank API Disabled"
    if balance_5 == "":
        balance_5 = "Bank API Disabled"
   
    # Update the balance labels for each tab
    update_balance_label(profile_0, balance_0)
    update_balance_label(profile_1, balance_1)
    update_balance_label(profile_2, balance_2)
    update_balance_label(profile_3, balance_3)
    update_balance_label(profile_4, balance_4)
    update_balance_label(profile_5, balance_5)
    transactions = skyblock_data.get("profiles", [])[selected_profile].get("banking", {}).get("transactions", [])[0:50]
    # Call the function with the extracted amounts
    create_transaction_graph(transactions)


def create_transaction_graph(transactions):
    # Extract transaction data
    amounts = [transaction['amount'] for transaction in transactions]
    initiators = [transaction['initiator_name'] for transaction in transactions]
    actions = [transaction['action'] for transaction in transactions]

    # Create dictionaries to store total amounts for each initiator
    initiator_totals = {}
    for amount, initiator, action in zip(amounts, initiators, actions):
        if initiator not in initiator_totals:
            initiator_totals[initiator] = {'amounts': [], 'color': np.random.rand(3,)}
        if action == 'DEPOSIT':
            initiator_totals[initiator]['amounts'].append(amount)
        elif action == 'WITHDREW':
            initiator_totals[initiator]['amounts'].append(-amount)

    # Create a line graph with different colors for each initiator
    plt.figure(figsize=(10, 6))
    for initiator, data in initiator_totals.items():
        plt.plot(data['amounts'], marker='o', linestyle='-', label=initiator, color=data['color'])

    plt.xlabel('Transaction Number')
    plt.ylabel('Transaction Amount')
    plt.title('Transaction Amounts by Initiator')
    plt.legend()
    plt.grid(True)
    # Customize the formatting of the y-axis tick labels
    formatter = ScalarFormatter(useMathText=False)
    formatter.set_scientific(False)  # Disable scientific notation
    formatter.set_powerlimits((-3, 3))  # Set the limits for when to use scientific notation

    plt.gca().yaxis.set_major_formatter(formatter)
    plt.show()






# Function to display JSON data in the Treeview widget
def display_data_in_treeview(data, parent=""):
    output_tree.delete(*output_tree.get_children(parent))
    for key, value in data.items():
        if isinstance(value, dict):
            sub_parent = output_tree.insert(parent, "end", text=key)
            output_tree.item(sub_parent, tags=("closed",))
            display_dict_in_treeview(value, sub_parent)
        elif isinstance(value, list):
            sub_parent = output_tree.insert(parent, "end", text=key)
            output_tree.item(sub_parent, tags=("closed",))
            display_list_in_treeview(value, sub_parent)
        else:
            # Check if the value is a number and format it with commas
            if isinstance(value, (int, float)):
                formatted_value = "{:,.0f}".format(value)
            else:
                formatted_value = value

            output_tree.insert(parent, "end", text=key, values=(formatted_value,))


# Function to display dictionary data in the Treeview widget
def display_dict_in_treeview(data, parent):
    for key, value in data.items():
        sub_parent = output_tree.insert(parent, "end", text=key)
        output_tree.item(sub_parent, tags=("closed",))
        if isinstance(value, dict):
            display_dict_in_treeview(value, sub_parent)
        elif isinstance(value, list):
            display_list_in_treeview(value, sub_parent)
        else:
            output_tree.insert(sub_parent, "end", text=key, values=(value,))


# Function to display list data in the Treeview widget
def display_list_in_treeview(data, parent):
    for index, item in enumerate(data):
        sub_parent = output_tree.insert(parent, "end", text=f"[{index}]")
        output_tree.item(sub_parent, tags=("closed",))
        if isinstance(item, dict):
            display_dict_in_treeview(item, sub_parent)
        elif isinstance(item, list):
            display_list_in_treeview(item, sub_parent)
        else:
            output_tree.insert(sub_parent, "end", text=f"[{index}]", values=(item,))


# Define a global variable to store auction data
auctions = []


# Function to fetch and store auction data
def fetch_auction_data():
    global auctions  # Access the global auctions variable

    hypixel_auctions_api_url = "https://api.hypixel.net/skyblock/auctions"
    response = requests.get(hypixel_auctions_api_url)

    if response.status_code == 200:
        auction_data = response.json()
        auctions = auction_data.get("auctions", [])  # Store the fetched data
        display_auction_data(auctions)  # Display the initial data
    else:
        auctions_tree.delete(*auctions_tree.get_children())
        auctions_tree.insert("", "end", values=("Error fetching data",))


def search_auctions():
    # Get the search term from the entry widget
    search_term = search_entry.get().strip().lower()

    # Filter the auction data based on the search term
    filtered_auctions = [
        auction
        for auction in auctions
        if search_term in auction.get("item_name", "").lower()
    ]

    # Display the filtered data
    display_auction_data(filtered_auctions)
    fetch_auction_data


def display_auction_data(auction_data):
    auctions_tree.delete(*auctions_tree.get_children())

    for auction in auction_data:
        item_name = auction.get("item_name", "Hypixel API Down")
        lore_text = auction.get("item_lore", "Hypixel API Down")
        starting_bid = auction.get("starting_bid", "Hypixel API Down")
        starting_bid = (
            "{:,}".format(starting_bid)
            if starting_bid != "Hypixel API Down"
            else starting_bid
        )
        highest_bid = auction.get("highest_bid_amount", "BIN")
        highest_bid = (
            "{:,}".format(highest_bid)
            if highest_bid != "Hypixel API Down"
            else highest_bid
        )
        if highest_bid == 0:
            highest_bid = "BIN"  # Replace 0 with "BIN"

        auctions_tree.insert(
            "", "end", values=(item_name, lore_text, starting_bid, highest_bid)
        )


# Create the main window
root = customtkinter.CTk()
root.title("Skyblock Peeker by: @retrodotexe")
pywinstyles.apply_style(root, "aero")


# Set the initial window size (width x height)
root.geometry("800x600")

# Create a Tabview
tabview = customtkinter.CTkTabview(master=root)
tabview.pack(fill="both", expand=True)

tabview.add("Home")
tabview.add("Player Stats")  # Add a "Player Stats" tab


# Create a Frame for the "Player Stats" tab
player_stats_frame = customtkinter.CTkFrame(master=tabview.tab("Player Stats"))
player_stats_frame.pack(fill=tk.BOTH, expand=True)

# Create a set to store the added tab names
added_tabs = set()

def display_transaction_graph(profile_name):
    # Retrieve the transactions for the specified profile_name
    selected_profile_index = list(added_tabs).index(profile_name)
    selected_profile = skyblock_data.get("profiles", [])[selected_profile_index]
    transactions = selected_profile.get("banking", {}).get("transactions", [])[0:50]

    # Call the function to create and display the transaction graph
    create_transaction_graph(transactions)

def profile_tabs(profile_0, profile_1, profile_2, profile_3, profile_4, profile_5, skyblock_data):
    # Remove any tabs that were previously added but are not in the current profiles
    for tab_name in added_tabs.copy():
        if tab_name not in {profile_0, profile_1, profile_2, profile_3, profile_4, profile_5}:
            profiletabs.delete(tab_name)
            added_tabs.remove(tab_name)
    for profile_name in [profile_0, profile_1, profile_2, profile_3, profile_4, profile_5]:
        if profile_name:
            if profile_name not in added_tabs:
                profiletabs.add(profile_name)
                added_tabs.add(profile_name)

                # Create a button for this profile tab
                graph_button = customtkinter.CTkButton(profiletabs.tab(profile_name), text="Show Graph",
                                                      command=lambda name=profile_name: display_transaction_graph(name),
                                                      font=("Helvetica", 12))
                graph_button.pack()

    # Call data_per_tab with the currently selected profile
    selected_profile = profiletabs.select()
    selected_profile_index = list(added_tabs).index(selected_profile)
    data_per_tab(skyblock_data, profile_0, profile_1, profile_2, profile_3, profile_4, profile_5, selected_profile_index)
    
    # Add new tabs with cute_names
    if profile_0 != "":
        if profile_0 not in added_tabs:
            profiletabs.add(profile_0)
            added_tabs.add(profile_0)
    if profile_1 != "":
        if profile_1 not in added_tabs:
            profiletabs.add(profile_1)
            added_tabs.add(profile_1)
    if profile_2 != "":
        if profile_2 not in added_tabs:
            profiletabs.add(profile_2)
            added_tabs.add(profile_2)
    if profile_3 != "":
        if profile_3 not in added_tabs:
            profiletabs.add(profile_3)
            added_tabs.add(profile_3)
    if profile_4 != "":
        if profile_4 not in added_tabs:
            profiletabs.add(profile_4)
            added_tabs.add(profile_4)
    if profile_5 != "":
        if profile_5 not in added_tabs:
            profiletabs.add(profile_5)
            added_tabs.add(profile_5)
    selected_profile = ""
    data_per_tab(skyblock_data, profile_0, profile_1, profile_2, profile_3, profile_4, profile_5, selected_profile)



# Create a label and an entry for the username
PlayerTitle = customtkinter.CTkLabel(
    master=player_stats_frame,
    text="Skyblock Peeker by: @retrodotexe",
    font=("Helvetica", 20),
)
PlayerTitle.pack()
username_entry = customtkinter.CTkEntry(
    master=player_stats_frame, font=("Helvetica", 12)
)
username_entry.pack()
fetch_button = customtkinter.CTkButton(
    master=player_stats_frame,
    text="Peek User",
    command=get_uuid,
    font=("Helvetica", 12),
)
fetch_button.pack()

profiletabs = customtkinter.CTkTabview(master=player_stats_frame)
profiletabs.pack(fill="both", expand=True)

###Treeview Customisation (theme colors are selected)
bg_color = root._apply_appearance_mode(
    customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
)
text_color = root._apply_appearance_mode(
    customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
)
selected_color = root._apply_appearance_mode(
    customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
)

treestyle = ttk.Style()
treestyle.theme_use("default")
treestyle.configure(
    "Treeview",
    background=bg_color,
    foreground=text_color,
    fieldbackground=bg_color,
    borderwidth=0,
)
treestyle.map(
    "Treeview",
    background=[("selected", bg_color)],
    foreground=[("selected", selected_color)],
)
root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())

def toggle_tree_frame():
    if tree_frame.winfo_viewable():
        tree_frame.pack_forget()
    else:
        tree_frame.pack(fill=tk.BOTH, expand=True)

toggle_button = customtkinter.CTkButton(player_stats_frame, text="Toggle Tree Frame (Great for developers learning the Hypixel API)", command=toggle_tree_frame)
toggle_button.pack()

# Create a Frame to contain the Treeview for "Player Stats"
tree_frame = customtkinter.CTkFrame(master=player_stats_frame)
tree_frame.pack(fill=tk.BOTH, expand=True)
tree_frame.pack_forget()

# Create a Treeview widget inside the "Player Stats" Frame
output_tree = ttk.Treeview(
    tree_frame, columns=("Value"), show="tree", selectmode="none"
)
output_tree.pack(fill=tk.BOTH, expand=True)

# Set the size of the Treeview widget
output_tree.heading("#1", text="Key")
output_tree.heading("Value", text="Value")

# Make the Frame expand to fill the available space
tree_frame.grid_propagate(False)


treeview_style = ttk.Style()
treeview_style.configure(
    "Custom.Treeview",
    background=bg_color,
    foreground=text_color,
    selectbackground=selected_color,
    selectforeground=text_color,
)

# Create a new tab for Auctions
tabview.add("Auctions")  # Add an "Auctions" tab
tabview.set("Auctions")  # Set "Auctions" as the active tab

# Create a Frame for the "Auctions" tab
auctions_frame = customtkinter.CTkFrame(master=tabview.tab("Auctions"))
auctions_frame.pack(fill=tk.BOTH, expand=True)

auctions_tree = ttk.Treeview(
    auctions_frame,
    columns=("Item", "Lore", "Starting Bid", "Highest Bid"),
    show="headings",
)
auctions_tree.heading("Item", text="Item")
auctions_tree.heading("Lore", text="Lore")
auctions_tree.heading("Starting Bid", text="Starting Bid")
auctions_tree.heading("Highest Bid", text="Highest Bid")

# Bind the show_item_details function to the Treeview widget
auctions_tree.bind("<Double-1>", show_item_details)


# Inside the "Auctions" tab creation section
search_label = customtkinter.CTkLabel(master=auctions_frame, text="Search Item:")
search_label.pack()
search_entry = customtkinter.CTkEntry(master=auctions_frame, font=("Helvetica", 12))
search_entry.pack()
search_button = customtkinter.CTkButton(
    master=auctions_frame,
    text="Search",
    command=search_auctions,
    font=("Helvetica", 12),
)
search_button.pack()

# Create a button to fetch auction data
fetch_auctions_button = customtkinter.CTkButton(
    master=auctions_frame,
    text="Fetch Auction Data",
    command=fetch_auction_data,
    font=("Helvetica", 12),
)
fetch_auctions_button.pack()


# Pack the Treeview and scrollbar
auctions_tree.pack(fill=tk.BOTH, expand=True)


tabview.set("Home")  # Set "Player Stats" as the active tab


# Start the Tkinter main loop
root.mainloop()