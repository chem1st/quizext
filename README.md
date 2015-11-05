# quizext
Quiz app with extended options like multiple question variants and several question types

Installation

1. 	add 'quizext' to INSTALLED_APPS
2. 	import quizext.urls in urls.py
3. 	add url(r'^q/', include(quizext.urls)) to urlpatterns
4. 	app requires jquery v.1.7 or higher. You might include 
	<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
	in <head>.
5. 	add <script src="{% static 'quizext/js/jquery.countdown.min.js' %}"></script>
	in <head>.
6. 	quizapp templates extends base.html by default, however of course you
	can override this.
	Add {% block quizext %}{% endblock %} to your base.html