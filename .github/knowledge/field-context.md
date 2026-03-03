# Field Context

Purpose: Document the MySQL schema for the `CrmField` table (active and deprecated
columns), the Java field API inventory (new and deprecated APIs), the current field
architecture files, and the Field Filter API guide including filtering strategies,
core APIs, scenario recommendations, predicate construction, and best practices.
Agents must load this file whenever a task involves field schema inspection, field
API selection, or filter predicate construction.

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

## Field Filter API — Comprehensive Guide

### What Is the Field Filter API?

The Field Filter API is a tool that allows you to fetch a list of fields by applying
specific, chainable filter conditions using `Predicate<AbstractField>` lambdas.
This enables meta-driven, efficient field retrieval based on business logic rather
than hard-coded field lists.

---

### Filtering Strategies

#### Whitelisted Filtering (Inclusion)

An **opt-in** strategy that includes only a specific set of fields. All other fields
are ignored. Use when you know the exact fields you need — safer because it prevents
unexpected new fields from being processed.

**Example 1 — Filter by Field ID:**
```java
Set<Long> requiredFieldIds = Set.of(101L, 102L, 105L);
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(requiredFieldIds);
```

**Example 2 — Filter by API Name:**
```java
Predicate<AbstractField> filter = field -> "channel".equals(field.getApiName());
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

**Example 3 — Filter by Metadata (e.g. indexed datetime fields):**
```java
Predicate<AbstractField> filter = field -> field.isIndexed() && field.getNewFieldType() == DATETIME;
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

#### Blacklisted Filtering (Exclusion)

An **opt-out** strategy that excludes certain fields and returns everything else.
Use for future-proofing: new fields are automatically included. Your code must be
prepared to handle any new fields that are not explicitly blocked.

**Example — Exclude computed fields:**
```java
Predicate<AbstractField> filter = field -> !field.isComputed();
List<AbstractField> fields = new OrgFieldAPIImpl().getAbstractFields(MODULE.TICKETS.getName(), departmentId, filter);
```

**Example — Custom fields, optionally excluding unused ones:**
```java
Predicate<AbstractField> filter = AbstractField::isCustomField;

if (!isUnUsedFieldsNeeded) {
    Long layoutId = layoutApi.getLayoutsByDepartmentIds(CrmConstants.MODULE_AGENT, null)
                             .get(0)
                             .getLayoutId();
    Set<Long> unUsedFieldIds = layoutApi.getUnUsedAbstractFieldsInLayout(layoutId)
                                        .stream()
                                        .map(AbstractField::getId)
                                        .collect(Collectors.toSet());
    filter = field -> field.isCustomField() && !unUsedFieldIds.contains(field.getFieldId());
}
return orgFieldApi.getAbstractFields(module, null, filter);
```

---

### Core Filtering APIs

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

### How to Choose the Right API

| Scenario | Recommended API | Reason |
|----------|----------------|--------|
| Criteria and Query Store — query construction | `OrgFieldAPI` | Configuration context; cannot use permission API |
| Criteria and Query Store — UI field listing | `LayoutFieldAPI` | Show fields from the layout in the UI |
| Table Views and Reports | `FieldPermissionAPI` | Field access must be restricted by user profile |
| Blueprint Transaction Forms | `LayoutFieldAPI` | Show fields associated with the ticket's layout |

---

### Constructing Filters with Predicates

Filters are `Predicate<AbstractField>` lambdas that evaluate to `true` (include) or
`false` (exclude).

**Recommended Filterable Properties of `AbstractField`:**

| Property | Method | Notes |
|----------|--------|-------|
| Internal state flag | `isInternalState()` | Fields used for internal system processes |
| Computed flag | `isComputed()` | Formula / calculated fields |
| Mandatory flag | `isMandatory()` | Fields that require a value |
| Sortable flag | `isSortable()` | Fields that support sorting |
| Basic flag | `isBasic()` | Out-of-the-box system fields |
| Identifier flag | `isIdentifier()` | Fields acting as unique identifiers |
| Source type | `getSourceType()` | Origin: `SYSTEM`, `CUSTOM`, etc. |
| Field type | `getNewFieldType()` | Use this — not `getType()`, `getFieldType()`, or `getUiType()` |
| API name | `getApiName()` | Use as last resort for specific field targeting |
| Custom field | `isCustomField()` | `true` if the field was created by a user |
| Indexed | `isIndexed()` | `true` if the field has a DB index |

---

### Best Practices for Predicate Construction

#### 1. Avoid Internal Metadata in Filters

Never use methods that expose internal structural details in predicates. They lead
to fragile logic that breaks when the underlying system changes.

| Method to Avoid        | Alternate |
|------------------------|-----------|
| `getTableName()`       | N/A — do not use |
| `getColumnName()`      | N/A — do not use |
| `getType()`            | `getNewFieldType()` |
| `getFieldType()`       | `getNewFieldType()` |
| `getUiType()`          | `getNewFieldType()` |
| `getUITypeForCreate()` | `getNewFieldType()` |
| `getFieldLabel()`      | `getApiName()` |

**Recommended:**
```java
new OrgFieldApiImpl().getAbstractFields(MODULE.TICKETS.getName(), null,
    field -> !field.isInternalState() && !field.isComputed());
```

**Problematic — Do NOT use:**
```java
var caseColumnNames = Set.of(CRMCASE.SUBJECT, ...);
var filter = field -> field.getTableName().equals(CRMCASE.TABLE)
                   && caseColumnNames.contains(field.getColumnName());
new OrgFieldApiImpl().getAbstractFields(MODULE.TICKETS.getName(), null, filter);
```

#### 2. Exclude Internal State Fields by Default

Almost every predicate should start by excluding internal state fields.
These fields (`responseSlaType`, `slaViolationType`, `isPresence`, etc.) are generally
not needed in UI or business logic.

```java
Predicate<AbstractField> filter = field -> !field.isInternalState() && /* additional conditions */;
```

#### 3. Limit the Use of Sets and Maps

Avoid building large `Set` or `Map` structures inside predicates unless absolutely
necessary. Prefer metadata-driven boolean flags on `AbstractField`.

#### 4. Use Expression Lambdas for Filtering

Prefer concise lambda expressions over anonymous inner classes to keep predicates
readable and composable.

```java
// Composable predicates
Predicate<AbstractField> notInternal = field -> !field.isInternalState();
Predicate<AbstractField> notComputed = field -> !field.isComputed();
Predicate<AbstractField> combined    = notInternal.and(notComputed);

List<AbstractField> fields = new OrgFieldAPIImpl()
    .getAbstractFields(MODULE.TICKETS.getName(), departmentId, combined);
```
