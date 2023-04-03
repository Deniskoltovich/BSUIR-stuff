from quaine import Minimizer

if __name__ == '__main__':
    formula = '((!x1+x2)*(x2=>x3))'
    match int(input('\t1 - Расчетный метод\n\t2 - Расчетно-табличный метод\n\t3 - Карно\n\t')):
        case 1:
            minimizer = Minimizer(f'{formula}', mode='CNF')
            minimizer.minimize_func_calculation_method()

            print(
                f'СКНФ: {minimizer.non_minimized_func}\nСокращенная КНФ: {minimizer.reduced_func}\nТупиковая КНФ: {minimizer.minimized_func}')
            minimizer = Minimizer(f'{formula}', mode='DNF')
            minimizer.minimize_func_calculation_method()
            print(
                f'СДНФ: {minimizer.non_minimized_func}\nСокращенная ДНФ: {minimizer.reduced_func}\nТупиковая ДНФ: {minimizer.minimized_func}')
        case 2:
            minimizer = Minimizer(f'{formula}', mode='CNF')
            minimizer.minimize_func_quine_method()
            print()
            print(
                f'СКНФ: {minimizer.non_minimized_func}\nСокращенная КНФ: {minimizer.reduced_func}\nТупиковая КНФ: {minimizer.minimized_func}')
            minimizer = Minimizer(f'{formula}', mode='DNF')
            minimizer.minimize_func_quine_method()
            print()
            print(
                f'СДНФ: {minimizer.non_minimized_func}\nСокращенная ДНФ: {minimizer.reduced_func}\nТупиковая ДНФ: {minimizer.minimized_func}')
        case 3:
            minimizer = Minimizer(f'{formula}', mode='CNF')
            minimizer.karnough_method()
            print(minimizer.print_karnough_table())
            print()
            print(
                f'СКНФ: {minimizer.non_minimized_func}\nСокращенная КНФ: {minimizer.reduced_func}\nТупиковая КНФ: {minimizer.minimized_func}')
            minimizer = Minimizer(f'{formula}', mode='DNF')
            minimizer.karnough_method()
            print()
            print(
                f'СДНФ: {minimizer.non_minimized_func}\nСокращенная ДНФ: {minimizer.reduced_func}\nТупиковая ДНФ: {minimizer.minimized_func}')
