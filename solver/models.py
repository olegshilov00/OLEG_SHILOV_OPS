from django.db import models

class QuadraticSolution(models.Model):
    a = models.FloatField()
    b = models.FloatField()
    c = models.FloatField()
    user_solution = models.CharField(max_length=255)
    correct_solution = models.CharField(max_length=255)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the solution in the form:
        "Solution for ax² + bx + c = 0"
        """
        return f"Solution for {self.a}x² + {self.b}x + {self.c} = 0"