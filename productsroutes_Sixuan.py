# MANAGE BOOKINGS
import shelve

import products_Sixuan
from products_Sixuan import Slots
from datetime import *
from Forms import PricingForm
from app import app
from flask import render_template, url_for, redirect, request, flash
from flask_wtf.csrf import validate_csrf


@app.route('/createSlot', methods=['GET', 'POST'])
def createSlot():
    d = datetime.now()
    form = PricingForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open("storage/slots") as slotsDb:
            if str(form.date.data) in slotsDb.keys():
                flash('Date already exists!')
                return redirect(url_for('createSlot'))

            elif form.date.data.day < d.year and form.date.data.month < d.month:
                flash('Date has passed!')
                return redirect(url_for('createSlot'))

            else:
                form.validate()
                slot = Slots(str(form.date.data))
                slot.setAdultPrice(form.adultPrice.data)
                slot.setConcessionPrice(form.concessionPrice.data)
                slot.setChildPrice(form.childPrice.data)
                slotsDb[str(form.date.data)] = slot
                return redirect(url_for('viewSlots'))
    return render_template('createSlot.html', form=form)


@app.route('/viewSlots')
def viewSlots():
    with shelve.open("storage/slots") as slotsDb:
        return render_template('viewSlots.html', slots_list=slotsDb)


@app.route('/updateSlot/<date>/', methods=['GET', 'POST'])
def updateSlot(date):
    form = PricingForm(request.form)
    if request.method == 'POST' and form.validate():
        with shelve.open("storage/slots") as slotsDb:
            slot = slotsDb.get(date)
            print(slot.getDate())
            slot.setAdultPrice(form.adultPrice.data)
            slot.setConcessionPrice(form.concessionPrice.data)
            slot.setChildPrice(form.childPrice.data)
            slot.setAvailability(0, form.availability1.data)
            slot.setAvailability(1, form.availability2.data)
            slot.setAvailability(2, form.availability3.data)
            slot.setAvailability(3, form.availability4.data)
            slot.setAvailability(4, form.availability5.data)
            print(slot.getAdultPrice())
            slotsDb[slot.getDate()] = slot
            return redirect(url_for('viewSlots'))
    else:
        with shelve.open("storage/slots") as slotsDb:
            slot = slotsDb.get(date)
            form.adultPrice.data = slot.getAdultPrice()
            form.concessionPrice.data = slot.getConcessionPrice()
            form.childPrice.data = slot.getChildPrice()
            return render_template('updateSlot.html', form=form)


@app.route('/deleteSlot/<date>', methods=['POST'])
def deleteSlot(date):
    with shelve.open("storage/slots") as slotsDb:
        slotsDb.pop(date)

    return redirect(url_for('viewSlots'))

@app.route('/clearSlots', methods=['POST'])
def clearSlots():
    with shelve.open("storage/slots") as slotsDb:
        slotsDb.clear()
    return redirect(url_for('viewSlots'))



@app.route('/makeAllAvailable/<date>', methods=['POST'])
def makeAllAvailable(date):
    with shelve.open("storage/slots") as slotsDb:
        print(date)
        slot = slotsDb[date]
        slot.setAvailability(0, 10)
        slot.setAvailability(1, 10)
        slot.setAvailability(2, 10)
        slot.setAvailability(3, 10)
        slot.setAvailability(4, 10)
        slot.makeAllAvailable()
        slotsDb[slot.getDate()] = slot


    return redirect(url_for('viewSlots'))


@app.route('/makeAllUnavailable/<date>', methods=['POST'])
def makeAllUnavailable(date):
    with shelve.open("storage/slots") as slotsDb:
        slot = slotsDb[date]
        slot.setAvailability(0, 0)
        slot.setAvailability(1, 0)
        slot.setAvailability(2, 0)
        slot.setAvailability(3, 0)
        slot.setAvailability(4, 0)
        slot.makeAllUnavailable()
        slotsDb[slot.getDate()] = slot
    return redirect(url_for('viewSlots'))
