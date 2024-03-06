demandsPerCent = {'Aged Meat':188,
                  'Bakers Basics':104,
                  'Barbecue Specialty':85,
                  'Basic Rations':73,
                  # 'Berry Basket':100,
                  'Brined Shank':36,
                  'Building Materials':85,
                  'Butcher\'s Box':45,
                  'Campfire Roast':73,
                  'Crafting Basics':80,
                #   'Crips Produce':100,
                  'Dairy Delivery':108,
                  # 'Exotic Fruits':100,
                  'Fried Chicken':187,
                  # 'Fruit Basket':100,
                  # 'General Spices':100,
                  'Glaceforde Explorers Kit':110,
                  # 'Juicers Box':100,
                  'Kabbar\'s Omelets':95,
                  'Kindling Kit':97,
                  'Margrove Ale Ingredients':186,
                  # 'Noble Delicacies':100,
                  'Pickled Vegetables':84,
                #   'Pie Making Kit':100,
                  'Ravencrest Finest Wears':78,
                  # 'Ravencrest Greens':100,
                  'Rohna Smoked Ham':188,
                  'Sailor\'s Remedy':77,
                  'Sajecho Fruit Basket':73,
                  'Sajecho\'s Spices':64,
                  'Seabreeze Rum':76,
                  'Settler\'s Rations':82,
                  'Slums Provisions':59,
                  'Sombreshade\'s Pie':105,
                  'Strawberry Cakes':118,
                  # 'Vegetable Stew':100,
                  'Winemakers Kit':133}

bonusPerCent = 0
route = 'Orca Bay - Defiance'
demands = {k:v/100 for k,v in demandsPerCent.items()}
bonusesPerCentChoices = [0,5,20,25,40,45]

def loadInputs():
    return demandsPerCent, bonusPerCent, route, demands, bonusesPerCentChoices