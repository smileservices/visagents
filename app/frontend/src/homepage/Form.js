import React, {useState, useEffect} from "react";
import ReactDOM from "react-dom";
import Select from 'react-select'
import {getCsrfToken} from "../../../src/components/utils";
import {list} from "../../../src/api_interface/list";

function UserForm({data, countryList, citiesList, onSubmit}) {
    const [formData, setFormData] = useState(data);
    const [alert, setAlert] = useState('');

    function validateForm(formData) {
        if (formData.nationality.length === 0) {
            setAlert('Please select your nationalities');
            return false;
        }
        if (!formData.city) {
            setAlert('Please select your city')
            return false;
        }
        return true;
    }

    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            if (validateForm(formData)) onSubmit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Quote</h2>
            <div className="form-group">
                <input key="form_name" type="text" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Full name"
                       value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})}/>
            </div>
            <div className="form-group">
                <input key="form_email" type="text" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Email"
                       value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})}
                />
            </div>
            <div className="form-group">
                <input key="form_phone" type="text" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Phone (optional)"
                       value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})}
                />
            </div>
            <div className="form-group">
                <div className="pb_select-wrap">
                    <Select
                        placeholder="Nationality"
                        options={countryList}
                        value={formData.nationality}
                        onChange={selectedOptions => setFormData({...formData, nationality: selectedOptions})}
                        isMulti
                    />
                </div>
            </div>
            <div className="form-group">
                <div className="pb_select-wrap">
                    <Select
                        placeholder="City"
                        options={citiesList}
                        value={formData.city}
                        onChange={selectedOptions => setFormData({...formData, city: selectedOptions})}
                    />
                </div>
            </div>
            {alert ? <div className="alert alert-danger">{alert}</div> : ''}
            <div className="form-group">
                <input type="submit" className="btn btn-primary btn-lg btn-block pb_btn-pill  btn-shadow-blue"
                       value="Next to step 2/3"/>
            </div>
        </form>
    )
}

function ServiceForm({data, servicesList, onSubmit, onBack}) {
    const [formData, setFormData] = useState(data);
    const [alert, setAlert] = useState('');

    function validateForm(formData) {
        if (!formData.service) {
            setAlert('Please select the visa service')
            return false;
        }
        return true;
    }

    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            if (validateForm(formData)) onSubmit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Quote</h2>
            <h3 className="mb-4 mt-0 text-center">Step 2/3</h3>
            <div className="form-group">
                <div className="pb_select-wrap">
                    <Select
                        placeholder="Service"
                        options={servicesList}
                        value={formData.service}
                        onChange={selectedOptions => setFormData({...formData, service: selectedOptions})}
                    />
                </div>
            </div>
            <div className="form-group">
                <label htmlFor="persons">How many persons:</label>
                <input required={true} id="persons" key="form_persons" type="int"
                       className="form-control pb_height-50 reverse"
                       placeholder="How many persons"
                       value={formData.persons} onChange={e => setFormData({...formData, persons: e.target.value})}/>
            </div>
            <div className="form-group">
                <textarea id="note" key="form_note" className="form-control pb_height-50 reverse"
                          placeholder="Note(optional)"
                          value={formData.note} onChange={e => setFormData({...formData, note: e.target.value})}/>
            </div>
            {alert ? <div className="alert alert-danger">{alert}</div> : ''}
            <div className="form-group">
                <input type="submit" className="btn btn-primary btn-lg btn-block pb_btn-pill  btn-shadow-blue"
                       value="Next to final step"/>
            </div>
            <div className="form-footer">
                <small>
                    <a href="" onClick={e => {
                        e.preventDefault();
                        onBack(formData);
                    }}><i className="fas fa-backward"> </i> back to step 1</a>
                </small>
            </div>
        </form>
    )
}

function VisaForm({data, onSubmit, onBack}) {
    const [formData, setFormData] = useState(data);
    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            onSubmit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Quote</h2>
            <h3 className="mb-4 mt-0 text-center">Step 3/3</h3>
            <div className="form-group">
                <label htmlFor="type">Visa type</label>
                <input required={true} id="type" key="form_visa_type" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Current visa type"
                       value={formData.type} onChange={e => setFormData({...formData, type: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Issue Place</label>
                <input required={true} id="issue_place" key="issue_place" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Where did the visa was issued"
                       value={formData.issue_place}
                       onChange={e => setFormData({...formData, issue_place: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Issue Date</label>
                <input required={true} id="issue_date" key="issue_date" type="date"
                       className="form-control pb_height-50 reverse"
                       placeholder="When did the visa was issued"
                       value={formData.issue_date}
                       onChange={e => setFormData({...formData, issue_date: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Visa Expiration Date</label>
                <input id="expiration" key="expiration" type="date" className="form-control pb_height-50 reverse"
                       placeholder="When will the visa expire"
                       value={formData.expiration}
                       onChange={e => setFormData({...formData, expiration: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="entry_port">Entry Port</label>
                <input required={true} id="entry_port" key="entry_port" type="text"
                       className="form-control pb_height-50 reverse"
                       placeholder="Where you entered Vietnam"
                       value={formData.entry_port}
                       onChange={e => setFormData({...formData, entry_port: e.target.value})}/>
            </div>
            <div className="form-group">
                <label htmlFor="issue_place">Entry Date</label>
                <input required={true} id="entry_date" key="entry_date" type="date"
                       className="form-control pb_height-50 reverse"
                       placeholder="When you entered Vietnam"
                       value={formData.entry_date}
                       onChange={e => setFormData({...formData, entry_date: e.target.value})}/>
            </div>
            <div className="form-group">
                <input type="submit" className="btn btn-primary btn-lg btn-block pb_btn-pill  btn-shadow-blue"
                       value="Submit"/>
            </div>
            <div className="form-footer">
                <small>
                    <a href="" onClick={e => {
                        e.preventDefault();
                        onBack(formData);
                    }}><i className="fas fa-backward"> </i> back to step 2</a>
                </small>
            </div>
        </form>
    )
}

function FormSubmitted({alert}) {
    return (
        <div className={"alert alert-" + alert.type}>{alert.text}</div>
    )
}

function QuoteForm() {
    const emptyUserData = {
        'name': 'vlad gorica',
        'email': 'mail@mail.com',
        'phone': '01283829884',
        'nationality': [{value: 'RO', label: 'Romania'}],
        'city': {value: '12', label: 'Danang'},
    }
    const emptyServiceData = {
        'service': {value: '3', label: 'Visa Extension 3 month'},
        'persons': 1,
        'note': ''
    }
    const emptyVisaData = {
        'type': 'turist visa',
        'issue_place': 'HCMC',
        'issue_date': '2020-01-20',
        'expiration': '2020-06-20',
        'entry_port': 'HCMC',
        'entry_date': '2020-01-20',
    }

    const [step, setStep] = useState(1);
    const [userData, setUserData] = useState(emptyUserData);
    const [serviceData, setServiceData] = useState(emptyServiceData);
    const [visaData, setVisaData] = useState(emptyVisaData);
    const [alert, setAlert] = useState({});

    const [countryList, setCountryList] = useState([]);
    const [servicesList, setServicesList] = useState([]);
    const [citiesList, setCitiesList] = useState([]);

    function get_countries() {
        fetch(DATA_ENDPOINT.countries, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setCountryList(data);
        })
    }

    function get_cities() {
        fetch(DATA_ENDPOINT.cities, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setCitiesList(data);
        })
    }

    function get_services() {
        fetch(DATA_ENDPOINT.services, {
            method: "GET"
        }).then(result => {
            //todo set waiting
            if (result.ok) {
                return result.json();
            } else {
                setAlert('Could not read data: ' + result.statusText)
            }
        }).then(data => {
            setServicesList(data);
        })
    }

    useEffect(() => {
        get_countries();
        get_cities();
        get_services();
    }, [])

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
                sentQuoteRequest(userData, serviceData, visaData);
                setStep(4);
            }} onBack={formData => {
                setVisaData(formData);
                setStep(2);
            }}/>
        case 4:
            return <FormSubmitted alert={alert}/>;
    }
}


const wrapper = document.getElementById("quote_form");
wrapper ? ReactDOM.render(<QuoteForm/>, wrapper) : null;