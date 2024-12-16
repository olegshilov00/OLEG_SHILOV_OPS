import math
import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.utils.crypto import get_random_string
from .models import QuadraticSolution

class MenuView(View):
    def get(self, request):
        """
        GET method for MenuView.

        This method renders the menu.html template.
        """
        return render(request, 'solver/menu.html')

class SolveView(View):
    def get(self, request):
        """
        GET method for SolveView.

        This method retrieves coefficients 'a', 'b', and 'c' from the request's query parameters,
        attempts to parse them as floats, and calculates the roots of the quadratic equation
        ax² + bx + c = 0. It handles special cases for linear equations and scenarios where
        coefficients might not be provided correctly. The results are rendered in the 'solve.html'
        template, which displays the equation and its roots or relevant error messages.

        Args:
            request: The HTTP request object containing query parameters 'a', 'b', and 'c'.

        Returns:
            HttpResponse: A response with the rendered 'solve.html' template.
        """

        a = request.GET.get("a", "0")
        b = request.GET.get("b", "0")
        c = request.GET.get("c", "0")

        try:
            a, b, c = float(a), float(b), float(c)

            if a == 0 and b == 0 and c == 0:
                roots = "Ошибка: уравнение не определено (все коэффициенты равны нулю)."
            elif a == 0:
                if b == 0:
                    roots = "Ошибка: коэффициенты 'a' и 'b' не могут быть равны нулю одновременно."
                else:
                    root = -c / b
                    roots = f"Корень линейного уравнения: x = {root}"
            else:
                discriminant = b**2 - 4 * a * c

                if discriminant > 0:
                    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                    roots = f"Корни уравнения: x1 = {root1}, x2 = {root2}"
                elif discriminant == 0:
                    root = -b / (2 * a)
                    roots = f"Корень уравнения: x = {root}"
                else:
                    roots = "Нет действительных корней"
        except ValueError:
            roots = "Ошибка: введены некорректные данные"

        context = {
            "equation": f"{a}x² + {b}x + {c} = 0",
            "roots": roots
        }
        return render(request, "solver/solve.html", context)

class TrainerView(View):
    def get(self, request):
        """
        Renders the trainer template with a quadratic equation for the user to solve.
        
        If the request contains a 'result', it retrieves the correctness status,
        the correct solution, and the user's solution from the query parameters.
        Otherwise, these values are set to None. Random coefficients for a new
        quadratic equation are generated and passed to the template.

        Args:
            request: The HTTP request object containing query parameters.

        Returns:
            HttpResponse: A response with the rendered 'trainer.html' template,
            including the coefficients of the equation and solution details.
        """

        if 'result' in request.GET:
            is_correct = (request.GET.get('is_correct') == 'True')
            correct_solution = request.GET.get('correct_solution', '')
            user_solution = request.GET.get('user_solution', '')
        else:
            is_correct = None
            correct_solution = None
            user_solution = None

        random_a = random.randint(1, 10)  
        random_b = random.randint(-10, 10)
        random_c = random.randint(-10, 10)

        return render(request, 'solver/trainer.html', {
            'a': random_a,
            'b': random_b,
            'c': random_c,
            'user_solution': user_solution,
            'correct_solution': correct_solution,
            'is_correct': is_correct
        })

    def post(self, request):
        """
        Handles POST requests to the trainer view.

        Retrieves the coefficients of the equation and user's solution from the request,
        calculates the correct solution, and checks if the user's solution is correct.
        Stores the result in the database, and redirects to the same view with the result
        as query parameters.
        
        If the request contains the 'solution' parameter with the value 'нет корней',
        it is assumed that the user has answered that the equation has no roots.
        
        Parameters:
            request: The HTTP request object containing query parameters.
        
        Returns:
            HttpResponse: A response with a redirect to the same view, with query
            parameters indicating the result of the user's answer.
        """
        a = float(request.POST['a'])
        b = float(request.POST['b'])
        c = float(request.POST['c'])

        root1_raw = request.POST.get('root1', '').replace(',', '.').strip()
        root2_raw = request.POST.get('root2', '').replace(',', '.').strip()

        if request.POST.get('solution') == "нет корней":
            user_solution = "нет корней"
            user_solution_list = []
        else:
            user_solution_list = list(filter(None, [root1_raw, root2_raw]))
            user_solution = ", ".join(user_solution_list)

        discriminant = b**2 - 4*a*c

        if discriminant < 0:
            correct_roots = None
        elif abs(discriminant) < 1e-15:
            correct_roots = [(-b) / (2*a)]
        else:
            r1 = (-b + math.sqrt(discriminant)) / (2*a)
            r2 = (-b - math.sqrt(discriminant)) / (2*a)
            correct_roots = sorted([r1, r2])

        if correct_roots is None:
            is_correct = (user_solution.lower() == "нет корней")
            correct_solution = "нет корней"
        else:
            if not user_solution_list:
                is_correct = False
            else:
                try:
                    user_vals = [float(x) for x in user_solution_list]
                except ValueError:
                    user_vals = []
                
                matched = [False]*len(correct_roots)
                is_correct_temp = True

                for uv_str, uv in zip(user_solution_list, user_vals):
                    d = max(len(uv_str.split('.')[-1]) if '.' in uv_str else 0, 2)

                    found_pair = False
                    for i, correct_val in enumerate(correct_roots):
                        if not matched[i] and abs(round(correct_val, d) - uv) < 1e-9:
                            matched[i] = True
                            found_pair = True
                            break
                    if not found_pair:
                        is_correct_temp = False
                        break
                
                if not all(matched):
                    is_correct_temp = False

                is_correct = is_correct_temp

            correct_solution_list = [f"{cr:.4f}" for cr in correct_roots]
            correct_solution = ", ".join(correct_solution_list)

        QuadraticSolution.objects.create(
            a=a, b=b, c=c,
            user_solution=user_solution,
            correct_solution=correct_solution,
            is_correct=is_correct
        )

        return redirect(
            f"{reverse('trainer')}?result=1&is_correct={is_correct}"
            f"&correct_solution={correct_solution}&user_solution={user_solution}"
        )
