# What's The Weather

![Splash](splash.jpg)

This is a command line application that queries the OpenWeatherMap API and displays the weather forecast in tabular 
format.  There are two reports - the current weather report and the daily weather report.

![Current Weather](current-weather.png)

The Current Weather Report.

![Daily Weather](daily-weather.png)

The Daily Weather Report.

## Libraries

The application uses the following libraries to build the command line interface and display the weather reports.

| Library  | Description                                |
|----------|--------------------------------------------|
| click    | Handles the command line parsing           |
| inquirer | Collects user input                        |
| rich     | Handles the display of the weather reports |

## Usage

Start by creating a virtual environment using an environment manager such as PIPENV to do so:

```
pipenv --python 3.10.5
```

Activate the environment and install the application:

```
pipenv shell
pipenv install git+https://github.com/dooley-ch/whatstheweather#egg=whatstheweather
```

Once the application has been installed, you can check the version number to ensure that it has been properly installed:

```
whatstheweather --version
```

Before making a weather query the application needs to be initialized and you need to add your OpenWeatherKey:

```
whatstheweather setup init
```

```
whatstheweather setup key 6***.........***2
```

Once you have completed these tasks, you can try a query:

```
whatstheweather report -c "New York" -cty USA  -u metric -s NY current
```

## Follow Up

A detailed commentary of this application can be found here: [Developer Notes](https://www.developernotes.org/2022/08/command-line-reference-application/)
 