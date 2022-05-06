import React, { useState } from 'react'
import django from 'django'

const getItemByValue = (items, value) => {
  return items.find(item => item.value === value)
}

export const Filter = (props) => {
  const [currFilterItem, setCurrFilterItem] =
    useState(getItemByValue(props.filterItems, props.selectedFilter))

  const onSelectFilter = (filterItem) => {
    setCurrFilterItem(filterItem)
    props.onFilterChange(filterItem.value)
  }

  return (
    <div className="mt-2 mt-sm-0">
      <div className="dropdown dropdown-menu-end">
        <button
          type="button"
          className="dropdown-toggle btn btn--light btn--select"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {django.gettext('Filter')}: {currFilterItem.label}
          <i className="fa fa-caret-down" aria-hidden="true" />
        </button>
        <ul className="dropdown-menu">
          {props.filterItems.map((filterItem, i) => (
            <li key={`${i}_${filterItem.label}`}>
              <button onClick={() => onSelectFilter(filterItem)}>
                {django.gettext(filterItem.label)}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
