import tkinter as tk

root = tk.Tk()
root.geometry("430x400")
root.title("ROI Calculator")

# ---------------------------------------
#  STYLES
# ---------------------------------------
TITLE_FONT = ("Segoe UI", 11, "bold")
LABEL_FONT = ("Segoe UI", 9)
FRAME_STYLE = {"bd": 2, "relief": "groove", "padx": 10, "pady": 10}


# ---------------------------------------
#  FRAMES
# ---------------------------------------
frame_crafting = tk.Frame(root, **FRAME_STYLE)
frame_crafting.grid(row=0, column=0, padx=15, pady=10, sticky="n")

frame_disenchant = tk.Frame(root, **FRAME_STYLE)
frame_disenchant.grid(row=0, column=1, padx=15, pady=10, sticky="n")

frame_bottom = tk.Frame(root)
frame_bottom.grid(row=1, column=0, columnspan=2, pady=10)


# ---------------------------------------
#  TITLES
# ---------------------------------------
tk.Label(frame_crafting, text="Crafting Materials", font=TITLE_FONT).grid(
    row=0, column=0, columnspan=3, pady=(0, 8))
tk.Label(frame_disenchant, text="Disenchant Results", font=TITLE_FONT).grid(
    row=0, column=0, columnspan=3, pady=(0, 8))


# ---------------------------------------
#  FUNCTIONS (unchanged)
# ---------------------------------------
def crafting(clean_craft_qty, clean_craft_price):
    mat_cost = []
    for i in range(len(clean_craft_qty)):
        cost = clean_craft_qty[i] * clean_craft_price[i]
        mat_cost.append(cost)
    craft_cost = sum(mat_cost)
    return mat_cost, craft_cost


def disenchant(clean_dis_chance, clean_dis_price):
    disenchant_drop = []
    for i in range(len(clean_dis_chance)):
        dis = clean_dis_chance[i] * clean_dis_price[i]
        disenchant_drop.append(dis)
    disenchant_total = sum(disenchant_drop)
    return disenchant_drop, disenchant_total


def roi(craft_cost, disenchant_total):
    profit = disenchant_total - craft_cost
    return (profit / craft_cost) * 100 if craft_cost != 0 else 0


def input_validation(entries_list):
    floated_numbers = []
    for entry in entries_list:
        strip_entries = entry.get().strip()
        if strip_entries == "":
            return "error: empty field"
        try:
            num_converted = float(strip_entries)
        except ValueError:
            return "error: numbers only"
        if num_converted < 0:
            return "error: negative numbers not allowed"
        floated_numbers.append(num_converted)
    return floated_numbers


# ---------------------------------------
#  CRAFTING GRID (qty, price)
# ---------------------------------------
entry_craft_qty = []
entry_craft_price = []

tk.Label(frame_crafting, text="Material",
         font=LABEL_FONT).grid(row=1, column=0, padx=3)
tk.Label(frame_crafting, text="Qty", font=LABEL_FONT).grid(row=1, column=1)
tk.Label(frame_crafting, text="Price", font=LABEL_FONT).grid(row=1, column=2)

for i in range(5):
    tk.Label(frame_crafting, text=f"Material {i+1}:",
             font=LABEL_FONT).grid(row=i+2, column=0, pady=3)

    qty = tk.Entry(frame_crafting, width=8)
    qty.grid(row=i+2, column=1, pady=3)
    qty.insert(0, "0")
    entry_craft_qty.append(qty)

    price = tk.Entry(frame_crafting, width=8)
    price.grid(row=i+2, column=2, pady=3)
    price.insert(0, "0")
    entry_craft_price.append(price)

label_craft_cost = tk.Label(
    frame_crafting, text="Crafting Cost : 0.00", font=LABEL_FONT)
label_craft_cost.grid(row=8, column=0, columnspan=3, pady=8)


# ---------------------------------------
#  DISENCHANT GRID
# ---------------------------------------
disenchant_chance = [0.75, 0.22, 0.03]
entry_disenchant_chance = []
entry_disenchant_price = []

tk.Label(frame_disenchant, text="Type", font=LABEL_FONT).grid(row=1, column=0)
tk.Label(frame_disenchant, text="Chance",
         font=LABEL_FONT).grid(row=1, column=1)
tk.Label(frame_disenchant, text="Price", font=LABEL_FONT).grid(row=1, column=2)

names = ["Dust", "Essence", "Crystal"]

for i in range(3):
    tk.Label(frame_disenchant, text=names[i] + ":",
             font=LABEL_FONT).grid(row=i+2, column=0, pady=3)

    chance = tk.Entry(frame_disenchant, width=8)
    chance.grid(row=i+2, column=1)
    chance.insert(0, disenchant_chance[i])
    entry_disenchant_chance.append(chance)

    price = tk.Entry(frame_disenchant, width=8)
    price.grid(row=i+2, column=2)
    price.insert(0, 0)
    entry_disenchant_price.append(price)

label_disenchant_total = tk.Label(
    frame_disenchant, text="Disenchant Total : 0.00", font=LABEL_FONT)
label_disenchant_total.grid(row=6, column=0, columnspan=3, pady=8)


# ---------------------------------------
#  CALCULATE BUTTON + ROI DISPLAY
# ---------------------------------------
label_error = tk.Label(frame_bottom, text=" ", fg="red",
                       font=("Segoe UI", 9, "bold"))
label_error.grid(row=0, column=0, columnspan=2, pady=5)


def on_calculate():
    clean_craft_qty = input_validation(entry_craft_qty)
    if isinstance(clean_craft_qty, str):
        label_error.config(text=clean_craft_qty)
        return

    clean_craft_price = input_validation(entry_craft_price)
    if isinstance(clean_craft_price, str):
        label_error.config(text=clean_craft_price)
        return

    clean_dis_chance = input_validation(entry_disenchant_chance)
    if isinstance(clean_dis_chance, str):
        label_error.config(text=clean_dis_chance)
        return

    clean_dis_price = input_validation(entry_disenchant_price)
    if isinstance(clean_dis_price, str):
        label_error.config(text=clean_dis_price)
        return

    label_error.config(text="")

    mat_cost, craft_cost = crafting(clean_craft_qty, clean_craft_price)
    label_craft_cost.config(text=f"Crafting Cost : {craft_cost:.2f}")

    disenchant_drop, disenchant_total = disenchant(
        clean_dis_chance, clean_dis_price)
    label_disenchant_total.config(
        text=f"Disenchant Total : {disenchant_total:.2f}")

    roiis = roi(craft_cost, disenchant_total)
    label_roi.config(text=f"ROI: {roiis:.2f}%")


button_calc = tk.Button(frame_bottom, text="Calculate",
                        width=10, command=on_calculate)
button_calc.grid(row=1, column=0, pady=5)

label_roi = tk.Label(frame_bottom, text="ROI: 0%",
                     font=("Segoe UI", 10, "bold"))
label_roi.grid(row=2, column=0, pady=5)

root.mainloop()
