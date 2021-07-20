import 'dart:js';

import 'package:app_arexsell/auth/auth_repository.dart';
import 'package:app_arexsell/auth/form_submission_status.dart';
import 'package:app_arexsell/auth/login/login_bloc.dart';
import 'package:app_arexsell/auth/login/login_event.dart';
import 'package:app_arexsell/auth/login/login_state.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LoginView extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocProvider(
          create: (context) =>
              LoginBloc(authRepo: context.read<AuthRepository>()),
          child: _loginForm()),
    );
  }

  Widget _loginForm() {
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 40),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            _userField(),
            _passwordField(),
            _loginButton(),
          ],
        ),
      ),
    );
  }

  Widget _userField() {
    return BlocBuilder<LoginBloc, LoginState>(builder: (context, state) {
      return TextFormField(
        decoration: InputDecoration(
          icon: Icon(Icons.person),
          hintText: "Usuário",
        ),
        validator: (value) => state.isValidUser ? null : "Nome muito curto",
        onChanged: (value) => context.read<LoginBloc>().add(
              LoginUserChanged(user: value),
            ),
      );
    });
  }

  Widget _passwordField() {
    return BlocBuilder<LoginBloc, LoginState>(builder: (context, state) {
      return TextFormField(
        obscureText: true,
        decoration: InputDecoration(
          icon: Icon(Icons.security),
          hintText: "Senha",
        ),
        validator: (value) =>
            state.isValidPassword ? null : "Senha muito curta",
        onChanged: (value) => context.read<LoginBloc>().add(
              LoginPasswordChanged(password: value),
            ),
      );
    });
  }

  Widget _loginButton() {
    return BlocBuilder<LoginBloc, LoginState>(builder: (context, state) {
      return state.formStatus is FormSubmitting
          ? CircularProgressIndicator()
          : ElevatedButton(
              onPressed: () {
                if (_formKey.currentState!.validate()) {
                  context.read<LoginBloc>().add(LoginSubmitted());
                }
              },
              child: Text("Login"),
            );
    });
  }
}
