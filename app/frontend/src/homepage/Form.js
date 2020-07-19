import React, {useState, useEffect} from "react";
import {getCsrfToken} from "../../../src/components/utils";
import {UserForm} from "./UserDataForm";
import {VisaForm} from "./VisaDataForm";
import {ServiceForm} from "./ServiceDataForm";


export function FormSubmitted({alert}) {
    return (
        <div className={"alert alert-" + alert.type}>{alert.text}</div>
    )
}

export function QuoteForm({countryList, citiesList, servicesList}) {
    const emptyUserData = {
        'name': '',
        'email': '',
        'phone': '',
        'nationality': [],
        'city': '',
    }
    const emptyServiceData = {
        'service': '',
        'persons': 1,
        'note': ''
    }
    const emptyVisaData = {
        'type': '',
        'issue_place': '',
        'issue_date': '',
        'expiration': '',
        'entry_port': '',
        'entry_date': '',
    }

    const [step, setStep] = useState(1);
    const [userData, setUserData] = useState(emptyUserData);
    const [serviceData, setServiceData] = useState(emptyServiceData);
    const [visaData, setVisaData] = useState(emptyVisaData);
    const [alert, setAlert] = useState({});


    function sentQuoteRequest(userData, serviceData, visaData) {
        setAlert({
            type: 'info',
            text: 'Submitting the form ...'
        });
        return fetch(QUOTE_REQUEST.post, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({
                userData: userData,
                serviceData: serviceData,
                visaData: visaData,
            })
        }).then(result => {
            if (result.ok) return result.json();
            setAlert({
                type: 'danger',
                text: 'Could not send the quote request: ' + result.statusText
            })
        }).then(data => {
            if (data.success) {
                setAlert({
                    type: 'success',
                    text: data.text
                })
            } else {
                setAlert({
                    type: 'danger',
                    text: data.text
                })
            }
        })
    }


    switch (step) {
        case 1:
            return <UserForm data={userData} countryList={countryList} citiesList={citiesList} onSubmit={formData => {
                setUserData(formData);
                setStep(2);
            }}/>
        case 2:
            return <ServiceForm data={serviceData} servicesList={servicesList} onSubmit={formData => {
                setServiceData(formData);
                setStep(3);
            }} onBack={formData => {
                setServiceData(formData);
                setStep(1);
            }}/>
        case 3:
            return <VisaForm data={visaData} onSubmit={formData => {
                setVisaData(formData);
                sentQuoteRequest(userData, serviceData, formData);
                setStep(4);
            }} onBack={formData => {
                setVisaData(formData);
                setStep(2);
            }}/>
        case 4:
            return <FormSubmitted alert={alert}/>;
    }
}