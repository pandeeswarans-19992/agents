# Field Context

Purpose: Document the MySQL schema for the `CrmField` table (active and deprecated
columns), the Java field API inventory (new and deprecated APIs), the current field
architecture files, the core filtering APIs, and the MySQL diagnostic query templates.
Agents must load this file whenever a task involves field schema inspection, field
API selection, or filter predicate construction.
For filtering strategies, predicate best practices, and scenario guidance,
refer to `.github/knowledge/filter-knowledge.md`.

---

## MySQL Schema — `CrmField` Table

Each row in the `CrmField` table represents one field belonging to a module.

### Active Columns

| Column               | Description |
|----------------------|-------------|
| `MODULEID`           | Foreign key referencing `ZD_Modules.MODULEID` |
| `FIELDID`            | Surrogate primary key |
| `COLUMNNAME`         | Physical database column name for the field's value |
| `TABLENAME`          | Physical database table that stores the field's value |
| `FIELDLABEL`         | Display label shown in the UI |
| `APINAME`            | API-level name used in predicates and programmatic access |
| `DECIMALDIGITS`      | Number of decimal places (for DECIMAL / CURRENCY fields) |
| `ROUNDINGPRECISION`  | Rounding precision (for DECIMAL / CURRENCY fields) |
| `ISENCRYPTED`        | `1` = field value is stored encrypted |
| `ACCESSPERMISSION`   | Bitmask controlling read / write access |
| `COLORCODE_STATUS`   | `1` = field supports colour-coded display |
| `SOURCE_TYPE`        | Origin of the field (`SYSTEM`, `CUSTOM`, etc.) |
| `TYPE`               | Field type identifier (replaces deprecated `UITYPE`) |
| `ISPRESENCE`         | `1` = field is present / active; `0` = field is hidden |
| `IS_COMPUTED`        | `1` = computed / formula field; cannot be used in filter predicates |
| `IS_SORTABLE`        | `1` = field supports sorting |
| `IS_BASIC`           | `1` = basic / system-provided field |
| `IS_INTERNAL_STATE`  | `1` = internal state field; excluded from Filter API by default |
| `IS_IDENTIFIER`      | `1` = field acts as a unique identifier for its module |
| `IS_INDEXED`         | `1` = field has a database index |
| `CREATEDBY`          | ID of the user who created the field |
| `CREATEDTIME`        | Timestamp when the field was created |
| `MODIFIEDBY`         | ID of the user who last modified the field |
| `MODIFIEDTIME`       | Timestamp when the field was last modified |
| `DEP_ID`             | Dependency ID linking the field to its module dependency entry |

### Deprecated Columns

The following columns are deprecated and must not be used in new queries or predicates.
Do not reference them in filter logic, diagnostic queries, or agent recommendations.

| Deprecated Column          | Notes |
|----------------------------|-------|
| `TABID`                    | Replaced by module-level identifiers |
| `SECTIONID`                | Layout section reference — no longer used |
| `RESERVED_COLUMN`          | Internal reservation column |
| `RESERVED_TABLE`           | Internal reservation table |
| `GENERATEDTYPE`            | Replaced by `SOURCE_TYPE` |
| `UITYPE`                   | Replaced by `TYPE` |
| `PRESENCE`                 | Replaced by `ISPRESENCE` |
| `FIELDSEQUENCE`            | Field ordering — managed at layout level |
| `READONLYTYPE`             | Read-only flag — replaced by `ACCESSPERMISSION` |
| `MAXIMUMLEN`               | Max length — enforced at application layer |
| `ISMANDATORY`              | Mandatory flag — managed at layout level |
| `ISQUICKCREATE`            | Quick-create flag — managed at layout level |
| `ISALPHABETICAL`           | Sorting hint — use `IS_SORTABLE` |
| `SHOWTYPE`                 | Display context bitmask — no longer used |
| `WEBTOCASE`                | Web-to-case flag — legacy feature |
| `FIELDDESC`                | Field description — not actively maintained |
| `TOOLTIPTYPE`              | Tooltip type — legacy UI feature |
| `TOOLTIP`                  | Tooltip text — legacy UI feature |
| `FEATURES`                 | Feature flags — replaced by specific boolean columns |
| `VALIDATION_TYPES`         | Validation flags — replaced by application-layer validators |
| `ISPHI`                    | PHI (Personal Health Information) flag — replaced by `ISENCRYPTED` |
| `UNIQUE_STATUS`            | Unique constraint flag — enforced at application layer |
| `TRACK_LAST_ACTIVITY_TIME` | Activity tracking flag — replaced by audit tables |
| `TRACK_FIELDID`            | Activity tracking field reference — replaced by audit tables |

---

## MySQL Schema — `ZD_Modules` Table

| Column       | Description |
|--------------|-------------|
| `MODULEID`   | Surrogate primary key |
| `NAME`       | Module display name |
| `SYSTEMNAME` | System / API name used in Filter API URLs and programmatic access |
| `PRESENCE`   | `1` = module is active; `0` = module is disabled globally |
| `SHOWTYPE`   | Bitmask controlling module visibility contexts |

---

## Java Field API Inventory

Base package: `com/zoho/support/core/fields/`

### New (Current) Field APIs

| File | Purpose |
|------|---------|
| `OrgFieldAPI.java` | Base API interface for fetching fields and picklist values |
| `OrgFieldAPIImpl.java` | Implementation of `OrgFieldAPI` |
| `FieldPermissionAPI.java` | API interface for field permissions |
| `FieldPermissionAPIImpl.java` | Implementation of `FieldPermissionAPI` |
| `LayoutFieldAPI.java` | API interface for layout fields and layout picklist values |
| `LayoutFieldAPIImpl.java` | Implementation of `LayoutFieldAPI` |

### Deprecated Field APIs

| File | Reason |
|------|--------|
| `FieldAPI.java` | Old Field API interface |
| `FieldAPIImpl.java` | Old Field API implementation |
| `FieldsUtil.java` | Old general utility |
| `FieldUtil.java` (in `com.adventnet.support.common.util`) | Old `getDataTypeInDB`, `FIELD_TYPES_SUPPORTED_FOR_NEW_FLOW` |
| `Field.java` | Old legacy field entity |
| `LayoutField.java` (in `com.zoho.support.core.fields`) | Old legacy layout field entity |
| `Fields.java` (in `com.zoho.desk.dataimport`) | Old constants class |
| `FieldType.LOOKUP` (id=16) in `FieldType.java` line 66 | Marked `@Deprecated` — use `LOOK_UP` (id=20) instead |
| `FieldType.HIDDEN_FIELD` (id=19) in `FieldType.java` line 74 | Marked `@Deprecated` |

---

## New (Current) Field Architecture Files

### Core Framework Files

| File | Purpose |
|------|---------|
| `AbstractField.java` | Base POJO for all fields |
| `FieldDBStore.java` | Base DB store for field CRUD |
| `BasicFieldValidator.java` | Common field meta validation |
| `AbstractFieldValueValidator.java` | Base value validator |
| `FieldValueValidator.java` | Value validator interface |
| `Validator.java` | Field validator interface |
| `FieldType.java` | Enum defining all field types |
| `FieldTypeStore.java` | Maps field type → DBStore, Validator, ValueValidator |
| `IFieldTypeStore.java` | FieldTypeStore interface |
| `FieldConstants.java` | Constants |
| `FieldErrorCode.java` | Error codes |
| `FieldException.java` | Exception class |
| `FieldMaxLength.java` | Max length enums |
| `FieldApplicationType.java` | Application type enum |
| `FieldDBAPI.java` | Field DB API interface |
| `FieldDBAPIImpl.java` | Field DB API implementation |
| `DeskFieldAPI.java` | Desk field API interface |
| `DeskFieldAPIImpl.java` | Desk field API implementation |
| `FieldResource.java` | REST resource |
| `FieldServiceUtil.java` | Service utility |
| `FieldsDBUtil.java` | DB utility |
| `OrgFieldConfig.java` | Org field config POJO |
| `OrgFieldUtil.java` | Org field utility |
| `OrganizationFieldService.java` (in `com.zoho.support.restapi`) | REST API service — `typeVsClass` mapping |
| `CustomFieldValueConvertor.java` (in `com.zoho.support.core`) | Value conversions |
| `FieldPool.java` | Field pool |
| `CustomFieldPool.java` | Custom field pool |
| `CustomDepartmentFieldPool.java` | Dept field pool |

### Per-Field-Type Files

#### TEXT (SingleLine)
| File | Path |
|------|------|
| `SingleLineField.java` | `singlelinefield/SingleLineField.java` |
| `SingleLineFieldDBStore.java` | `singlelinefield/SingleLineFieldDBStore.java` |
| `SingleLineFieldValueValidator.java` | `singlelinefield/SingleLineFieldValueValidator.java` |

#### NUMBER (Integer)
| File | Path |
|------|------|
| `IntegerField.java` | `integerfield/IntegerField.java` |
| `IntegerFieldDBStore.java` | `integerfield/IntegerFieldDBStore.java` |
| `IntegerFieldValueValidator.java` | `integerfield/IntegerFieldValueValidator.java` |

#### PERCENT
| File | Path |
|------|------|
| `PercentField.java` | `percent/PercentField.java` |
| `PercentFieldDBStore.java` | `percent/PercentFieldDBStore.java` |
| `PercentFieldValueValidator.java` | `percent/PercentFieldValueValidator.java` |

#### DECIMAL
| File | Path |
|------|------|
| `DecimalField.java` | `decimal/DecimalField.java` |
| `DecimalFieldDBStore.java` | `decimal/DecimalFieldDBStore.java` |
| `DecimalFieldValidator.java` | `decimal/DecimalFieldValidator.java` |
| `DecimalFieldValueValidator.java` | `decimal/DecimalFieldValueValidator.java` |
| `LayoutDecimalFieldDBStore.java` | `decimal/LayoutDecimalFieldDBStore.java` |

#### CURRENCY
| File | Path |
|------|------|
| `CurrencyField.java` | `currency/CurrencyField.java` |
| `CurrencyFieldDBStore.java` | `currency/CurrencyFieldDBStore.java` |
| `CurrencyFieldValidator.java` | `currency/CurrencyFieldValidator.java` |
| `CurrencyFieldValueValidator.java` | `currency/CurrencyFieldValueValidator.java` |
| `LayoutCurrencyFieldDBStore.java` | `currency/LayoutCurrencyFieldDBStore.java` |
| `CurrencyFieldDBAPI.java` | `currency/CurrencyFieldDBAPI.java` |
| `CurrencyFieldDBAPIImpl.java` | `currency/CurrencyFieldDBAPIImpl.java` |

#### DATE
| File | Path |
|------|------|
| `DateField.java` | `date/DateField.java` |
| `DateFieldDBStore.java` | `date/DateFieldDBStore.java` |
| `DateFieldValueValidator.java` | `date/DateFieldValueValidator.java` |

#### DATETIME
| File | Path |
|------|------|
| `DateTimeField.java` | `datetime/DateTimeField.java` |
| `DateTimeFieldDBStore.java` | `datetime/DateTimeFieldDBStore.java` |
| `DateTimeFieldValueValidator.java` | `datetime/DateTimeFieldValueValidator.java` |

#### EMAIL
| File | Path |
|------|------|
| `EmailField.java` | `emailfield/EmailField.java` |
| `EmailFieldDBStore.java` | `emailfield/EmailFieldDBStore.java` |
| `EmailFieldValueValidator.java` | `emailfield/EmailFieldValueValidator.java` |

#### PHONE
| File | Path |
|------|------|
| `PhoneField.java` | `phonefield/PhoneField.java` |
| `PhoneFieldDBStore.java` | `phonefield/PhoneFieldDBStore.java` |
| `PhoneFieldValueValidator.java` | `phonefield/PhoneFieldValueValidator.java` |

#### ENUM (Picklist) & ARRAY (Multiselect)
| File | Path |
|------|------|
| `PickListField.java` | `picklist/PickListField.java` |
| `PickListFieldDBStore.java` | `picklist/PickListFieldDBStore.java` |
| `PicklistValidator.java` | `picklist/PicklistValidator.java` |
| `LayoutPickListFieldDBStore.java` | `picklist/LayoutPickListFieldDBStore.java` |
| `LayoutPickListValidator.java` | `picklist/LayoutPickListValidator.java` |
| `PickListFieldDBAPI.java` | `picklist/PickListFieldDBAPI.java` |
| `PickListFieldDBAPIImpl.java` | `picklist/PickListFieldDBAPIImpl.java` |
| `PickListFieldUtil.java` | `picklist/PickListFieldUtil.java` |
| `PickListFieldSubType.java` | `picklist/PickListFieldSubType.java` |

#### URL
| File | Path |
|------|------|
| `URLField.java` | `url/URLField.java` |
| `URLFieldDBStore.java` | `url/URLFieldDBStore.java` |
| `URLFieldValueValidator.java` | `url/URLFieldValueValidator.java` |

#### MULTI_LINE_TEXT (Textarea)
| File | Path |
|------|------|
| `MultiLineField.java` | `multilinefield/MultiLineField.java` |
| `MultiLineFieldDBStore.java` | `multilinefield/MultiLineFieldDBStore.java` |
| `MultiLineFieldValueValidator.java` | `multilinefield/MultiLineFieldValueValidator.java` |

#### BOOLEAN (Checkbox)
| File | Path |
|------|------|
| `CheckBoxField.java` | `checkbox/CheckBoxField.java` |
| `CheckBoxFieldDBStore.java` | `checkbox/CheckBoxFieldDBStore.java` |
| `LayoutCheckBoxFieldDBStore.java` | `checkbox/LayoutCheckBoxFieldDBStore.java` |
| `CheckboxDBAPI.java` | `checkbox/CheckboxDBAPI.java` |
| `CheckBoxDBAPIImpl.java` | `checkbox/CheckBoxDBAPIImpl.java` |

#### LOOK_UP (New Lookup)
| File | Path |
|------|------|
| `LookUpField.java` | `lookupfield/LookUpField.java` |
| `LookUpFieldDBStore.java` | `lookupfield/LookUpFieldDBStore.java` |
| `LookUpFieldValidator.java` | `lookupfield/LookUpFieldValidator.java` |
| `LayoutLookUpFieldDBStore.java` | `lookupfield/LayoutLookUpFieldDBStore.java` |
| `LayoutLookUpFieldValidator.java` | `lookupfield/LayoutLookUpFieldValidator.java` |
| `LookUpFieldDBAPI.java` | `lookupfield/LookUpFieldDBAPI.java` |
| `LookupFieldDBAPIImpl.java` | `lookupfield/LookupFieldDBAPIImpl.java` |

#### FORMULA
| File | Path |
|------|------|
| `FormulaField.java` | `formulafield/FormulaField.java` |
| `FormulaFieldDBStore.java` | `formulafield/FormulaFieldDBStore.java` |
| `FormulaFieldValidator.java` | `formulafield/FormulaFieldValidator.java` |
| `LayoutFormulaFieldDBStore.java` | `formulafield/LayoutFormulaFieldDBStore.java` |
| `LayoutFormulaFieldValidator.java` | `formulafield/LayoutFormulaFieldValidator.java` |
| `FormulaFieldDBAPI.java` | `formulafield/FormulaFieldDBAPI.java` |
| `FormulaFieldDBAPIImpl.java` | `formulafield/FormulaFieldDBAPIImpl.java` |
| `FormulaFieldUtil.java` | `formulafield/FormulaFieldUtil.java` |

#### Miscellaneous Field Types (use `MiscellaneousFieldDBStore`)

These field types share `MiscellaneousField` and `MiscellaneousFieldDBStore`:

| Field Type     | Enum ID |
|----------------|---------|
| FAX            | 17 |
| AUTONUMBER     | 15 |
| MULTI_LOOKUP   | 21 |
| PID            | 22 |
| EXPRESSION     | 23 |
| AUTO_NUMBER    | 24 |
| COLLECTION     | 25 |
| LARGE_TEXT_SYS | 26 |
| FILE_UPLOAD    | 27 |
| LARGE_TEXT     | 28 |

Shared files: `miscellaneous/MiscellaneousField.java`, `miscellaneous/MiscellaneousFieldDBStore.java`

### Supporting Sub-packages

| Sub-package               | Key Files |
|---------------------------|-----------|
| `expressions/`            | `ExpressionAPI.java`, `ExpressionDBAPI.java`, `ExpressionUtils.java`, `ExpressionExecutorAPI.java`, `SignupExpressionHandler.java` (18 files total) |
| `autonumber/`             | `AutonumberAPI.java`, `AutonumberGenerator.java`, `AutonumberResetAPI.java`, `AutonumberUtil.java` |
| `watchfields/`            | `WatchFieldAPI.java`, `WatchFieldDBAPI.java`, `WatchFieldValidator.java`, `WatchFieldMicrozHandler.java` (8 files total) |
| `largetext/`              | `LargeTextFieldAPINew.java`, `LargeTextFieldValueNew.java`, `LargeTextFieldValueValidator.java`, `LargeTextDBStoreAPI.java` (14 files total) |
| `conditionalAnnotations/` | `Condition.java`, `ConditionFactory.java`, `ConditionNode.java`, `FieldLevel.java`, `NeededFlag.java` |
| `converters/`             | `DOConverters.java`, `LayoutFieldDOConverter.java` |
| `license/`                | `LicenseFieldFeatureHandlerImpl.java`, `LicenseUniqueFieldFeatureHandlerImpl.java`, `LicensePhiFieldFeatureHandlerImpl.java` |
| `scheduler/`              | `CustomFieldDeletionBean.java`, `CustomFieldDeletionBeanImpl.java` |
| `encryptedFields/`        | `SystemFieldValueDeleteScheduler.java` |
| `unique/`                 | `UniqueFieldUtil.java`, `UniqueFieldScheduler.java` |

### Key Distinction: `large_text/` vs `largetext/`

- **`large_text/`** — Older package (`LargeTextFieldAPI`, `LargeTextFieldValue`, `LargeTextFieldAPIImpl`, etc.). Being replaced.
- **`largetext/`** — Newer package (`LargeTextFieldAPINew`, `LargeTextFieldValueNew`, `LargeTextFieldValueValidator`, etc.). Use this.

---

## Core Filtering APIs

#### OrgFieldAPI

Fetches fields based on module and department.
- Module **without** department → returns only organisation-level fields.
- Module **with** department → returns organisation-level and department-specific fields.

**Allowed Methods:**
1. `new OrgFieldAPIImpl().getAbstractFields(String module, Long departmentId, Predicate<AbstractField> filter)`
2. `new OrgFieldAPIImpl().getAbstractFields(Set<Long> fieldIds)` — use when you only have field IDs.

#### FieldPermissionAPI

Controls field access based on user profiles (Administrator, Agent, Light Agent).
`profileId` is mandatory for every call.

**Allowed Methods:**
1. `new FieldPermissionAPIImpl().getFieldProfilePermissions(String moduleName, Long profileId, Long departmentId, Predicate<FieldPermission> predicate)`
   — Retrieves `FieldPermission` objects for fields directly associated with a department.
2. `new FieldPermissionAPIImpl().getLayoutAssociatedFieldPermissionsInDepartments(String module, List<Long> departmentIds, Long profileId, Predicate<FieldPermission> fieldFilterPredicate)`
   — Retrieves `FieldPermission` objects for fields associated with layouts in the specified departments.

#### LayoutFieldAPI

Fetches fields associated with a specific layout. Use when customising forms for
record creation.

**Allowed Methods:**
1. `getLayoutFields(Long layoutId, Predicate<LayoutField> layoutFieldPredicate)` — fields for a single layout.
2. `getFieldIdsForLayouts(Set<Long> layoutIds)` — all field IDs from a set of layout IDs.

---

## Constructing Filters with Predicates

Filters are `Predicate<AbstractField>` lambdas that evaluate to `true` (include) or
`false` (exclude).

**Filter Syntax Example:**
```java
// This predicate filters out fields that are for internal state management.
Predicate<AbstractField> filter = (AbstractField field) -> !field.isInternalState();
```

---

## MySQL Diagnostic Query Templates

Agents must use these parameterised templates when executing diagnostic queries.
Always replace `?` with the actual module API name or field name from the user request.
Never expose credentials in reports; reference them from the environment config only.

### Q-01 — Resolve MODULEID from SYSTEMNAME

```sql
SELECT MODULEID, NAME, SYSTEMNAME, PRESENCE
FROM ZD_Modules
WHERE SYSTEMNAME = ?;
```

### Q-02 — Check all filter properties for a specific field

```sql
SELECT f.FIELDID, f.APINAME, f.TYPE,
       f.ISPRESENCE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.APINAME = ?;
```

### Q-03 — List all present/active fields for a module

```sql
SELECT f.APINAME, f.TYPE,
       f.ISPRESENCE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.ISPRESENCE = 1
ORDER BY f.APINAME;
```

### Q-04 — List hidden fields for a module

```sql
SELECT f.APINAME, f.TYPE,
       f.ISPRESENCE
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.ISPRESENCE = 0
ORDER BY f.APINAME;
```

### Q-05 — List internal state and computed fields for a module

```sql
SELECT f.APINAME, f.TYPE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED, f.ISPRESENCE
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND (f.IS_INTERNAL_STATE = 1 OR f.IS_COMPUTED = 1)
ORDER BY f.APINAME;
```

### Q-06 — Check ACCESSPERMISSION bitmask for a specific field

```sql
SELECT f.FIELDID, f.APINAME, f.TYPE,
       f.ACCESSPERMISSION, f.ISPRESENCE,
       f.IS_INTERNAL_STATE, f.IS_COMPUTED
FROM CrmField f
INNER JOIN ZD_Modules m ON f.MODULEID = m.MODULEID
WHERE m.SYSTEMNAME = ?
  AND f.APINAME = ?;
```

> **ACCESSPERMISSION bitmask guidance:**
> - `0` = no access restriction (field is visible to all profiles)
> - Non-zero value = access is restricted by profile bitmask; verify the caller's profile ID
>   has the corresponding bit set before concluding that the field is available via the Filter API.
> - Use in conjunction with `FieldPermissionAPI` to check profile-level visibility.

