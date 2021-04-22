import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class Settings extends StatefulWidget {
  Settings({Key key}) : super(key: key);

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Container(
                alignment: Alignment.centerLeft,
                padding: EdgeInsets.all(20),
                child: TextButton.icon(
                  label: Text(
                    'back',
                    style: TextStyle(fontSize: 15),
                  ),
                  style: TextButton.styleFrom(
                      padding: EdgeInsets.fromLTRB(0, 20, 20, 0),
                      alignment: Alignment.centerRight),
                  onPressed: () => {Navigator.pop(context)},
                  icon: Icon(Icons.arrow_back)6,
                )),
            Container(
                padding: EdgeInsets.fromLTRB(20, 5, 20, 0),
                height: MediaQuery.of(context).size.height * 0.8,
                child: Column(
                  children: [
                    Container(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Settings',
                        style: TextStyle(
                            fontSize: 25, fontWeight: FontWeight.bold),
                      ),
                    )
                  ],
                ))
          ],
        ),
      ),
    );
  }
}