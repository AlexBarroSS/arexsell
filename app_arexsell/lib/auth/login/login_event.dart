abstract class LoginEvent {}

class LoginUserChanged extends LoginEvent {
  final String user;

  LoginUserChanged({required this.user});
}

class LoginPasswordChanged extends LoginEvent {
  final String password;

  LoginPasswordChanged({required this.password});
}

class LoginSubmitted extends LoginEvent {}
