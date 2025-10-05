# crud_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Student
from .forms import StudentForm, Hobby_choices

def student_list(request):
    """
    Show list + search + filters. Also renders empty create form.
    Filters use GET so URLs are shareable/bookmarkable.
    """
    students = Student.objects.all()

    # SEARCH by name (GET param: q)
    q = request.GET.get('q', '')
    if q:
        students = students.filter(name__icontains=q)

    # FILTER by gender (GET param: gender)
    gender = request.GET.get('gender', '')
    if gender:
        students = students.filter(gender=gender)

    # FILTER by hobby (GET param: hobby may repeat)
    selected_hobbies = request.GET.getlist('hobby')  # list of codes like ['python','java']
    if selected_hobbies:
        # OR logic: any matching hobby
        qobj = Q()
        for h in selected_hobbies:
            qobj |= Q(hobbies__icontains=h)
        students = students.filter(qobj).distinct()

    form = StudentForm()  # blank form for create
    return render(request, 'crud_app/student_simple.html', {
        'students': students,
        'form': form,
        'q': q,
        'gender': gender,
        'selected_hobbies': selected_hobbies,
        'hobby_choices': Hobby_choices,
        'gender_choices': Student.Gender_choices,
    })

def student_create(request):
    """Handle POST from create form then redirect back to list."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        # If invalid, show list with the form errors
        students = Student.objects.all()
        return render(request, 'crud_app/student_simple.html', {
            'students': students,
            'form': form,
            'hobby_choices': Hobby_choices,
            'gender_choices': Student.Gender_choices
        })
    return redirect('student_list')

def student_update(request, id):
    """Show edit form (GET) and handle update (POST)."""
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')

    # GET or invalid POST -> render page showing this form prefilled
    students = Student.objects.all()
    return render(request, 'crud_app/student_simple.html', {
        'students': students,
        'form': form,
        'update_id': student.id,
        'hobby_choices': Hobby_choices,
        'gender_choices': Student.Gender_choices,
    })

def student_delete(request, id):
    """Delete on POST only."""
    if request.method == 'POST':
        student = get_object_or_404(Student, id=id)
        student.delete()
    return redirect('student_list')
