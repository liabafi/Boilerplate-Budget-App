class Category:

  def __init__(self, ct):
    self.ct = ct
    self.ledger = []
    self.balance = 0

  def get_balance(self):
    return self.balance

  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True

  def deposit(self, amount, description=""):

    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount

  def withdraw(self, amount, description=""):

    if not self.check_funds(amount):
      return False
    else:
      self.ledger.append({"amount": -amount, "description": description})
      self.balance -= amount

      return True

  def total_withdrawals(self):
    total_taken = 0

    for item in range(len(self.ledger)):
      if str(self.ledger[item]["amount"])[0] == "-":
        total_taken += abs(self.ledger[item]["amount"])
      else:
        continue

    return total_taken

  def transfer(self, amount, category):

    if not self.check_funds(amount):
      return False

    else:
      self.withdraw(amount, description=f"Transfer to {category.ct}")
      category.deposit(amount, description=f"Transfer from {self.ct}")

      return True

  def __repr__(self):

    first_line = self.ct.center(30, "*") + "\n"

    item_list = [
      self.ledger[i]["description"][:23] + str(
        ('%7.2f' % self.ledger[i]["amount"]
         )[:7]).rjust(30 - len(self.ledger[i]["description"]))
      for i in range(len(self.ledger))
    ]
    item_list_str = ("\n").join(item_list) + "\n"

    total_line = "Total: " + str('%.2f' % self.balance)

    return first_line + item_list_str + total_line


def create_spend_chart(categories):
  first_line = "Percentage spent by category" + "\n"

  #get total balance for every category, within withdrawals
  total_balance = 0

  for category in categories:
    for item in range(len(category.ledger)):
      if str(category.ledger[item]["amount"])[0] == "-":
        total_balance += abs(category.ledger[item]["amount"])
      else:
        continue

  #we need to know percentage for each Category
  ratios = [
    int((i.total_withdrawals() / total_balance * 100) / 10) * 10
    for i in categories
  ]

  if 100 in ratios:
    for index in range(len(ratios)):
      if ratios[index] != 100:
        ratios[index] = 0
      else:
        continue

  #generate labels
  labels = list(range(0, 110, 10))
  labels_formatted = [str(label) + "|" for label in labels]
  labels.reverse()
  labels_formatted.reverse()

  #generate bar chart values- to do
  label_string = ""

  for i in range(len(labels_formatted)):
    label_string += labels_formatted[i].rjust(4) + " "

    for j in range(len(categories)):
      if ratios[j] >= labels[i]:
        label_string += "o  "
      else:
        label_string += "   "

    label_string += "\n"

  #generate dash line
  total_num_spaces = 2 * len(categories) + 2
  dash_line = "    " + "-" * total_num_spaces + "--" + "\n"

  #generate category_names
  words_list = [str(category.ct) for category in categories]
  max_len = max([len(word) for word in words_list])
  words_list_padded = [
    word + " " * (max_len - len(word)) for word in words_list
  ]

  category_name_string = "     "

  for i in range(max_len):
    for word in words_list_padded:
      category_name_string += word[i] + "  "
    if i < max_len - 1:
      category_name_string += "\n     "
    else:
      continue

  return first_line + label_string + dash_line + category_name_string
