import React, {useState} from "react";
import Select from "react-select";

export function ServiceForm({data, servicesList, onSubmit, onBack}) {
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