   
def getUserChoice(validChoices: dict, allow_blank = False):
    while True:
        if allow_blank:
            print('Please enter one of the following choices, or leave blank:' )
        else:
            print('Please enter one of the following choices:' )

        print('\n'.join((map(lambda k: str(k[0]) + ' : ' + str(k[1]), validChoices.items()))))

        choice = input('>> ')
        if allow_blank:
            if choice == '' or choice.isspace():
                return choice
        
        if choice not in validChoices:
            print('Invalid selection, please try again')
        else:
            return choice

def getUserFloat(msg = 'enter a number >> '):
    while True:
        try:
            user_input = float(input(msg))
            return user_input
        except:
            print('input must be numeric or decimal')

class RentalProperty():
    class CashFlowItem():
        def __init__(self, primary_source = 0.0, additional_sources = dict()):
            self.primary_source = primary_source
            self.additional_sources = additional_sources

        def getTotal(self):
            value = self.primary_source
            for v in self.additional_sources.values():
                value += v
            return value

        def _getAllSourcesStrings(self):
            string = []
            for k, v in self.additional_sources.items():
                string.append(f'{k} - ' + '${:,.2f}'.format(v))
            return string

        def printAllSources(self):
            for s in self._getAllSourcesStrings():
                print(s)

        def _getPrimaryValueString(self):
            string = '${:,.2f}'.format(self.primary_source)
            return string

        def printPrimaryValue(self):
            string = self._getPrimaryValueString()
            print(string)

        def _getTotalString(self):
            return '${:,.2f}'.format(self.getTotal())

        def printTotalAmount(self):
            print(self._getTotalString())

        def printTotal(self):
            print(self._getTotalString())
            self.printPrimaryValue()
            self.printAllSources()

        def _userSet(self, msg = ''):
            source = getUserFloat(msg)
            if source < 0:
                print('Value cannot be negative')
            else:
                self.primary_source = source

        def userSet(self):
            self._userSet(msg='Enter a value')

        def _userAddName(self, msg = ''):
            name = input(msg)
            if name != '' and not name.isspace():
                return name

        def _userAddValue(self, name, msg):
            if name != '' and not name.isspace():
                value = getUserFloat(msg)
                if value < 0:
                    print('Value cannot be negative')
                elif value == 0:
                    print('Cancelling...')
                else:
                    if name in self.additional_sources.keys():
                        print('This entry already exists... Overwriting...')
                    self.additional_sources[name] = value

        def _userAdd(self, msg_name, msg_value):
            name = self._userAddName(msg_name)
            self._userAddValue(name, msg_value)

        def userAdd(self):
            self._userAdd(
                msg_name = 'Enter a name for this, or leave blank', 
                msg_value = 'Enter a value for this, or type 0 to cancel'
                )

        def _userRemove(self):
            name = getUserChoice(self.additional_sources, allow_blank=True)
            if name != '' and not name.isspace():
                del self.additional_sources[name]
                print(f'{name} has been removed')

        def userRemove(self):
            self._userRemove()

    class Income(CashFlowItem):
        def __init__(self, rental_income = 0.0, extra_sources = dict()):
            super().__init__(primary_source = rental_income, additional_sources = extra_sources)

        def _getTotalString(self):
            return 'Total monthly income: ' + super()._getTotalString()

        def _getPrimaryValueString(self):
            return '\tIncome from rent: ' + super()._getPrimaryValueString()

        def _getAllSourcesStrings(self):
            return list(map(lambda x: '\tMonthly income from: ' + x, super()._getAllSourcesStrings()))

        def userSet(self):
            super()._userSet(msg='Enter monthly rental income for this property >> $')

        def userAdd(self):
            super()._userAdd(
                msg_name = 'Enter the name of the income source, or leave blank to cancel >>', 
                msg_value = 'Enter monthly income amount for this source, or enter 0 to cancel >> $'
                )
        
        def userRemove(self):
            print('Enter the name of an income source to remove, or leave blank to cancel >> ')
            super().userRemove()

    class Expenses(CashFlowItem):
        def __init__(self, property_taxes = 0.0, additional_expenses = dict()):
            super().__init__(property_taxes, additional_expenses)

        def _getTotalString(self):
            return 'Total monthly expenses: ' + super()._getTotalString()

        def _getPrimaryValueString(self):
            return '\tMonthly expenses from property taxes: ' + super()._getPrimaryValueString()

        def _getAllSourcesStrings(self):
            return list(map(lambda x: '\tMonthly expenses from: ' + x, super()._getAllSourcesStrings()))

        def userSet(self):
            self._userSet(msg='Enter monthly property tax >> $')

        def userAdd(self):
            self._userAdd(
                msg_name = 'Enter the name of the expense, or leave blank to cancel >>', 
                msg_value = 'Enter monthly cost for this expense, or enter 0 to cancel >> $'
                )
        
        def userRemove(self):
            print('Enter the name of a monthly expense to remove, or leave blank to cancel >> ')
            super().userRemove()

    class InvestmentCost(CashFlowItem):
        def __init__(self, down_payment = 0.0, other = dict()):
            super().__init__(down_payment, other)

        def _getTotalString(self):
            return 'Total investment cost: ' + super()._getTotalString()

        def _getPrimaryValueString(self):
            return '\tDown Payment cost: ' + super()._getPrimaryValueString()

        def _getAllSourcesStrings(self):
            return list(map(lambda x: '\tAdditional cost of: ' + x, super()._getAllSourcesStrings()))

        def userSet(self):
            self._userSet(msg='Enter down payment cost for this property >> $')

        def userAdd(self):
            self._userAdd(
                msg_name = 'Enter the name of a one-time cost, or leave blank to cancel >>', 
                msg_value = 'Enter the amount of this cost, or enter 0 to cancel >> $'
                )
        
        def userRemove(self):
            print('Enter the name of an investment cost to remove, or leave blank to cancel >> ')
            super().userRemove()

        def userAddCost(self):
            self._userAddSecondarySource(msg_name = 'Enter the name of the additional investment cost, or leave blank to cancel >> ',
            msg_value = 'Enter amount, or enter 0 to cancel >> $', 
            msg_negative= 'Amount cannot be negative, cancelling...', 
            msg_overwrite= 'Cost already exists... overwriting...')

        def userRemoveCost(self):
            self._userRemoveSecondarySource(msg='Enter the name of the cost to remove, or leave blank to cancel >>')

    def __init__(self, name = ''):
        self.name = name
        self.income = self.Income()
        self.investment_cost = self.InvestmentCost()
        self.expenses = self.Expenses()

    def getMonthlyCashFlow(self):
        return self.income.getTotal() - self.expenses.getTotal()

    def getAnnualCashFlow(self):
        return self.getMonthlyCashFlow() * 12

    def getReturnOnInvestment(self):
        try:
            roi_pct = self.getAnnualCashFlow() / self.investment_cost.getTotal()
            roi_pct *= 100.00
            return roi_pct
        except:
            return 0.00

    def printMonthlyCashFlow(self):
        print('Monthly Cash Flow: ' + '${:,.2f}'.format(self.getMonthlyCashFlow()))
    
    def printAnnualCashFlow(self):
        print('Annual Cash Flow: ' + '${:,.2f}'.format(self.getAnnualCashFlow()))

    def printReturnOnInvestment(self):
        if self.investment_cost.getTotal() == 0:
            print('Missing investment cost; Cannot calculate return on investment')
        else:
            print(f'Return On Investment: {self.getReturnOnInvestment()}%')

    def printCashFlowRoI(self):
        self.printMonthlyCashFlow()
        self.printAnnualCashFlow()
        self.investment_cost.printTotalAmount()
        self.printReturnOnInvestment()

class ROICalculator():
    def __init__(self):
        self.rentalProperty = RentalProperty()
        self.exit_app = False

    def _userModifyCashFlowItem(self, msg_set, msg_add, msg_remove, cash_flow_item: RentalProperty.CashFlowItem):
        exit = False
        choices = {
            'set' : msg_set,
            'add' : msg_add,
            'remove' : msg_remove,
            'back' : 'Return to previous menu'
        }

        while not exit:
            cash_flow_item.printTotal()
            choice = getUserChoice(choices)

            if choice == 'set':
                cash_flow_item.userSet()
            elif choice == 'add':
                cash_flow_item.userAdd()
            elif choice == 'remove':
                cash_flow_item.userRemove()
            elif choice == 'back':
                exit = True

    def modifyIncome(self):
        self._userModifyCashFlowItem(
            'Sets the monthly rental income on this property', 
            'Adds an additional income source to this property, such as laundry',
            'Removes an income source from this property',
            self.rentalProperty.income
            )

    def modifyExpenses(self):
        self._userModifyCashFlowItem(
            'Sets the monthly tax cost for this property', 
            'adds an additional monthly expense to this property, such as insurance',
            'Removes an expense from this property',
            self.rentalProperty.expenses
            )

    def modifyInvenstmentCost(self):
        self._userModifyCashFlowItem(
            'Sets the down payment for this property', 
            'Adds an additional invenstment cost to this property, such as closing cost or needed repairs',
            'Removes a cost from this property',
            self.rentalProperty.investment_cost
            )

    def quit(self):
        print('Thank you for using this calculator')

    def run(self):
        choices = {
            'income' : 'View or modify this property\'s montly income sources and amount',
            'expenses' : 'View or modify monthly expenses for this property',
            'costs' : 'View or modify the one-time investment costs for this property',
            'view' : 'print monthly and annual cash flow for this property, and its return on investment %',
            'quit' : 'exit this program'
        }
        while not self.exit_app:
            choice = getUserChoice(choices)
            if choice == 'income':
                self.modifyIncome()
            elif choice == 'expenses':
                self.modifyExpenses()
            elif choice == 'costs':
                self.modifyInvenstmentCost()
            elif choice == 'view':
                self.rentalProperty.printCashFlowRoI()
            elif choice == 'quit':
                self.exit_app = True

        self.quit()


calculator = ROICalculator()
calculator.run()
