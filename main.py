   
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

        def _getTotal(self):
            value = self.primary_source
            for v in self.additional_sources.values():
                value += v
            return value

        def _printTotal(self, total_msg = '', primary_msg = '', additional_msg = ''):
            print(total_msg + ': ${:,.2f}'.format(self._getTotal()))
            print('\t' + primary_msg + ': ${:,.2f}'.format(self.primary_source))
            for k, v in self.additional_sources.items():
                print( '\t' + additional_msg + f' {k}: ' + '${:,.2f}'.format(v))
        
        def _userSetPrimarySource(self, msg = '', msg_negative = ''):
            source = getUserFloat(msg)
            if source < 0:
                print(msg_negative)
            else:
                self.primary_source = source

        def _userAddSecondarySource(self, msg_name = '', msg_value = '', msg_negative = '', msg_overwrite = ''):
            name = input(msg_name)
            if name != '' and not name.isspace():
                value = getUserFloat(msg_value)
                if value < 0:
                    print(msg_negative)
                elif value == 0:
                    print('Cancelling...')
                else:
                    if name in self.additional_sources.keys():
                        print(msg_overwrite)
                    self.additional_sources[name] = value

        def _userRemoveSecondarySource(self, msg = ''):
            print('msg')
            name = getUserChoice(self.additional_sources, allow_blank=True)
            if name != '' and not name.isspace():
                del self.additional_sources[name]
                print(f'{name} has been removed')

    class Income(CashFlowItem):
        def __init__(self, rental_income = 0.0, extra_sources = dict()):
            super().__init__(primary_source = rental_income, additional_sources = extra_sources)

        @property
        def rental_income(self):
            return self.primary_source

        @rental_income.setter
        def rental_income(self, value):
            self.primary_source = value

        def getTotalMonthlyIncome(self):
            return self._getTotal()

        def printMonthlyIncome(self):
            self._printTotal(total_msg='Total monthly income', primary_msg='Income from rent',
                additional_msg='Monthly income from')
        
        def userSetMonthlyRentalIncome(self):
            self._userSetPrimarySource(msg='Enter monthly rental income for this property >> $',
                msg_negative='Monthly rent cannot be negative... Cancelling...')

        def userAddIncomeSource(self):
            self._userAddSecondarySource(msg_name = 'Enter the name of the income source, or leave blank to cancel >> ',
            msg_value = 'Enter monthly income amount for this source, or enter 0 to cancel >> $', 
            msg_negative= 'Income amount cannot be negative, cancelling...', 
            msg_overwrite= 'Income source already exists... overwriting...')

        def userRemoveIncomeSource(self):
            self._userRemoveSecondarySource(msg='Enter the name of an income source to remove, or leave blank to cancel >>')

    class Expenses(CashFlowItem):
        def __init__(self, property_taxes = 0.0, additional_expenses = dict()):
            super().__init__(property_taxes, additional_expenses)

        @property
        def property_taxes(self):
            return self.primary_source

        @property_taxes.setter
        def property_taxes(self, value):
            self.primary_source = value

        @property
        def additional_expenses(self):
            return self.additional_sources

        @additional_expenses.setter
        def additional_expenses(self, value):
            self.additional_sources = value

        def getTotalMonthlyExpenses(self):
            return self._getTotal()

        def printMonthlyExpenses(self):
            self._printTotal(total_msg='Total monthly expenses', primary_msg='Monthly expenses for property taxes:',
                additional_msg='Monthly expenses for property taxes')

        def userSetMonthlyPropertyTaxes(self):
            self._userSetPrimarySource(msg='Enter monthly property taxes for this property >> $',
                msg_negative='Monthly taxes cannot be negative... Cancelling...')

        def userAddExpense(self):
            self._userAddSecondarySource(msg_name = 'Enter the name of the monthly expense, or leave blank to cancel >> ',
            msg_value = 'Enter monthly cost for this expense, or enter 0 to cancel >> $', 
            msg_negative= 'Amount cannot be negative, cancelling...', 
            msg_overwrite= 'Expense already exists... overwriting...')

        def userRemoveExpense(self):
            self._userRemoveSecondarySource(msg='Enter the name of the expense to remove, or leave blank to cancel >>')

    class InvestmentCost(CashFlowItem):
        def __init__(self, down_payment = 0.0, other = dict()):
            super().__init__(down_payment, other)

        def getTotalInvestmentCost(self):
            return self._getTotal()

        @property
        def down_payment(self):
            return self.primary_source

        @down_payment.setter
        def down_payment(self, value):
            self.primary_source = value

        @property
        def other(self):
            return self.additional_sources

        @other.setter
        def other(self, value):
            self.additional_sources = value
 
        def printTotalInvestmentCost(self):
            self._printTotal(total_msg='Total investment cost', primary_msg='Down payment',
                additional_msg='Total of all other costs')

        def userSetDownPayment(self):
            self._userSetPrimarySource(msg='Enter down payment for this property >> $',
                msg_negative='Cost cannot be negative... Cancelling...')

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
        return self.income.getTotalMonthlyIncome() - self.expenses.getTotalMonthlyExpenses()

    def getAnnualCashFlow(self):
        return self.getMonthlyCashFlow() * 12

    def getReturnOnInvestment(self):
        try:
            roi_pct = self.getAnnualCashFlow() / self.investment_cost.getTotalInvestmentCost()
            roi_pct *= 100.0
            return roi_pct
        except:
            return 0.0

    def printMonthlyCashFlow(self):
        print(f'Monthly Cash Flow: {self.getMonthlyCashFlow()}')
    
    def printAnnualCashFlow(self):
        print(f'Annual Cash Flow: {self.getAnnualCashFlow()}')

    def printReturnOnInvestment(self):
        if self.investment_cost.getTotalInvestmentCost() == 0:
            print('Missing investment cost; Cannot calculate return on investment')
        else:
            print(f'Return On Investment: {self.getReturnOnInvestment()}%')

    def printCashFlowRoI(self):
        self.printMonthlyCashFlow()
        self.printAnnualCashFlow()
        self.investment_cost.printTotalInvestmentCost()
        self.printReturnOnInvestment()

class ROICalculator():
    def __init__(self):
        self.rentalProperty = RentalProperty()
        self.exit_app = False

    def run(self):
        choices = {
            'income' : 'View or modify this property\'s montly income sources and mount',
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

    def _userModifyCashFlowItem(self, msg_set, msg_add, msg_remove, func_set, func_add, func_remove, func_print):
        exit = False
        choices = {
            'set' : msg_set,
            'add' : msg_add,
            'remove' : msg_remove,
            'exit' : 'Return to previous menu'
        }

        while not exit:
            func_print()
            choice = getUserChoice(choices)

            if choice == 'set':
                func_set()
            elif choice == 'add':
                func_add()
            elif choice == 'remove':
                func_remove()
            elif choice == 'exit':
                exit = True

    def modifyIncome(self):
        self._userModifyCashFlowItem(msg_set='Sets the monthly rental income on this property', 
            msg_add='Adds an additional income source to this property, such as laundry',
            msg_remove='Removes an income source from this property', 
            func_set=self.rentalProperty.income.userSetMonthlyRentalIncome, 
            func_add=self.rentalProperty.income.userAddIncomeSource, 
            func_remove=self.rentalProperty.income.userRemoveIncomeSource,
            func_print=self.rentalProperty.income.printMonthlyIncome)

    def modifyExpenses(self):
        self._userModifyCashFlowItem(msg_set='Sets the monthly tax cost for this property', 
            msg_add = 'adds an additional monthly expense to this property, such as insurance',
            msg_remove='Removes an expense from this property', 
            func_set=self.rentalProperty.expenses.userSetMonthlyPropertyTaxes, 
            func_add=self.rentalProperty.expenses.userAddExpense, 
            func_remove=self.rentalProperty.expenses.userRemoveExpense,
            func_print=self.rentalProperty.expenses.printMonthlyExpenses)

    def modifyInvenstmentCost(self):
        self._userModifyCashFlowItem(msg_set='Sets the down payment for this property', 
            msg_add = 'Adds an additional invenstment cost to this property, such as closing cost or needed repairs',
            msg_remove='Removes a cost from this property', 
            func_set=self.rentalProperty.investment_cost.userSetDownPayment, 
            func_add=self.rentalProperty.investment_cost.userAddCost, 
            func_remove=self.rentalProperty.investment_cost.userRemoveCost,
            func_print=self.rentalProperty.investment_cost.printTotalInvestmentCost)

    def quit(self):
        print('Thank you for using this calculator')


calculator = ROICalculator()
calculator.run()