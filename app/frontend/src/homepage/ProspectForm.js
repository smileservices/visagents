import React, {useState} from "react";
import Select from "react-select";
import {getCsrfToken} from "../../../src/components/utils";
import {FormSubmitted} from "./Form";

export function ProspectForm({citiesList}) {
    const emptyForm = {
        name: '',
        city: '',
        email: ''
    }
    const [formData, setFormData] = useState(emptyForm)
    const [alert, setAlert] = useState('');
    const [submitted, setSubmitted] = useState(false);

    function validateForm(formData) {
        if (!formData.city) {
            setAlert('Please select your city. Free prospects can choose only one.')
            return false;
        }
        return true;
    }

    function submit(formData) {
        setSubmitted(true);
        setAlert({
            type: 'info',
            text: 'Submitting the form ...'
        });
        return fetch(AGENCY.registerProspect, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify(formData)
        }).then(result => {
            if (result.ok) return result.json();
            setAlert({
                type: 'danger',
                text: 'Could not send the request: ' + result.statusText
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

    if (submitted) return <FormSubmitted alert={alert} />

    return (
        <form action="#" className="bg-white rounded pb_form_v1" onSubmit={e => {
            e.preventDefault();
            if (validateForm(formData)) submit(formData);
        }}>
            <h2 className="mb-4 mt-0 text-center">Free Register</h2>
            <div className="form-group">
                <input key="form_name" type="text" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Agency Name"
                       value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})}/>
            </div>
            <div className="form-group">
                <input key="form_email" type="email" className="form-control pb_height-50 reverse" required={true}
                       placeholder="Email"
                       value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})}
                />
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
                       value="Submit"/>
            </div>
        </form>
    )
}