import { useState, useEffect } from "react";
import { Form } from "react-bootstrap";
import Select from "react-select";

export default function MultiSelectDropdown({ options, onSelect }) {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const selectOptions = options.map((option) => ({
    value: option,
    label: option,
  }));

  const handleSelectChange = (selected) => {
    const selectedValues = selected
      ? selected.map((option) => option.value)
      : [];
    setSelectedOptions(selectedValues);
  };

  useEffect(() => {
    onSelect(selectedOptions);
  }, [selectedOptions, onSelect]);

  return (
    <>
      <Select
        placeholder="Select"
        isMulti
        closeMenuOnSelect={false}
        options={selectOptions}
        value={selectOptions.filter((option) =>
          selectedOptions.includes(option.value)
        )}
        onChange={handleSelectChange}
      ></Select>
    </>
  );
}
