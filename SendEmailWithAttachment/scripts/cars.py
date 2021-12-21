#!/usr/bin/env python3
import json
import locale
import os
import sys
import reports
import emails


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_total_sales={"total_sales":0}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    if item["total_sales"]>max_total_sales["total_sales"]:
      max_total_sales["car_model"]=item["car"]["car_model"]
      max_total_sales["total_sales"]=item["total_sales"]
      
    
    
    # TODO: also handle most popular car_year
  car_year={}
  popular_year=data[0]["car"]["car_year"]
  for car in data:
    year=car["car"]["car_year"] 
    if(year in car_year):
      car_year[year][0]+=1
      car_year[year][1]+=car["total_sales"]
    else:
      car_year[year]=[1,car["total_sales"]]
    if(car_year[year][0]> car_year[popular_year][0]):
      popular_year=year
  summary = [
    "The {} generated the most revenue: ${}".format(
      format_car(max_revenue["car"]), max_revenue["revenue"]), 
    "The {} had the most sales: {}".format(
      max_total_sales["car_model"],max_total_sales["total_sales"]),
    "The most popular year was {} with {} sales.".format(
      popular_year,car_year[popular_year][1]
    )
    
  ]

  return summary


def cars_dict_to_table(car_data):
  """Turns the data in car_data into a list of lists."""
  table_data = [["ID", "Car", "Price", "Total Sales"]]
  for item in car_data:
    table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
  return table_data


def main(argv):
  """Process the JSON data and generate a full report out of it."""
  data = load_data("../car_sales.json")
  summary = process_data(data)
  print(summary)
  # TODO: turn this into a PDF report
  table_data = [
    ["ID","Car","Price","Total Sales"]
    
  ]
  for x in data:
    table_data.append([x["id"],format_car(x["car"]),x["price"],x["total_sales"]])
                      
  reports.generate("/tmp/cars.pdf","Car summery Report",summary[0]+"<br/>"+
                   summary[1]+"<br/>"+summary[2]
                   ,table_data)
  # TODO: send the PDF report as an email attachment
  sender = "automation@example.com"
  receiver = "{}@example.com".format(os.environ.get('USER'))
  subject = "Sales summary for last month"
  body = "{}\n{}\n{}".format(*summary)

  message = emails.generate(sender, receiver, subject, body, "/tmp/cars.pdf")
  emails.send(message)


if __name__ == "__main__":
  main(sys.argv)
