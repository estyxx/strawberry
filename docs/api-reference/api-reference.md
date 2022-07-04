# API Reference

This page contains the full reference to Strawberry’s API.

<!--
\`\`\`{eval-rst}
.. autofunction:: strawberry.field
\`\`\` -->

### _class_ strawberry.enum.EnumDefinition(wrapped_cls: enum.EnumMeta, name: str, values: List[strawberry.enum.EnumValue], description: Optional[str])

### _class_ strawberry.BasePermission()

Bases: `object`

Base class for creating permissions

### _class_ strawberry.LazyType(type_name: str, module: str, package: Optional[str])

Bases: `Generic`[`strawberry.lazy_type.TypeName`, `strawberry.lazy_type.Module`]

### _class_ strawberry.Schema(query: Type, mutation: Optional[Type] = None, subscription: Optional[Type] = None, directives: Sequence[strawberry.directive.StrawberryDirective] = (), types=(), extensions: Sequence[Union[Type[strawberry.extensions.base_extension.Extension], strawberry.extensions.base_extension.Extension]] = (), execution_context_class: Optional[Type[graphql.execution.execute.ExecutionContext]] = None, config: Optional[strawberry.schema.config.StrawberryConfig] = None, scalar_overrides: Optional[Dict[object, Union[strawberry.custom_scalar.ScalarWrapper, strawberry.custom_scalar.ScalarDefinition]]] = None)

Bases: `strawberry.schema.base.BaseSchema`

#### introspect()

Return the introspection query result for the current schema

- **Raises**

  **ValueError** – If the introspection query fails due to an invalid schema

### strawberry.enum(\_cls: Optional[strawberry.enum.EnumType] = None, \*, name=None, description=None)

Registers the enum in the GraphQL type system.

If name is passed, the name of the GraphQL type will be
the value passed of name instead of the Enum class name.

### strawberry.field(resolver=None, \*, name=None, is_subscription=False, description=None, permission_classes=None, deprecation_reason=None, default=UNSET, default_factory=UNSET, directives=(), init=None)

Annotates a method or property as a GraphQL field.

This is normally used inside a type declaration:

```python
>>> @strawberry.type:
>>> class X:
>>>     field_abc: str = strawberry.field(description="ABC")
```

```python
>>>     @strawberry.field(description="ABC")
>>>     def field_with_resolver(self) -> str:
>>>         return "abc"
```

it can be used both as decorator and as a normal function.

### strawberry.input(cls=None, \*, name=None, description=None, directives=())

Annotates a class as a GraphQL Input type.
Example usage:

> > > @strawberry.input:
> > > class X:
> > > field_abc: str = “ABC”

### strawberry.interface(cls: Optional[Type] = None, \*, name: Optional[str] = None, description: Optional[str] = None, directives: Optional[Sequence[object]] = ())

Annotates a class as a GraphQL Interface.
Example usage:

> > > @strawberry.interface:
> > > class X:
> > > field_abc: str

### strawberry.mutation(resolver=None, \*, name=None, is_subscription=False, description=None, permission_classes=None, deprecation_reason=None, default=UNSET, default_factory=UNSET, directives=(), init=None)

Annotates a method or property as a GraphQL field.

This is normally used inside a type declaration:

```python
>>> @strawberry.type:
>>> class X:
>>>     field_abc: str = strawberry.field(description="ABC")
```

```python
>>>     @strawberry.field(description="ABC")
>>>     def field_with_resolver(self) -> str:
>>>         return "abc"
```

it can be used both as decorator and as a normal function.

### strawberry.scalar(cls=None, \*, name: Optional[str] = None, description: Optional[str] = None, specified_by_url: Optional[str] = None, serialize: Callable = <function identity>, parse_value: Optional[Callable] = None, parse_literal: Optional[Callable] = None)

Annotates a class or type as a GraphQL custom scalar.

Example usages:

```python
>>> strawberry.scalar(
>>>     datetime.date,
>>>     serialize=lambda value: value.isoformat(),
>>>     parse_value=datetime.parse_date
>>> )
```

```python
>>> Base64Encoded = strawberry.scalar(
>>>     NewType("Base64Encoded", bytes),
>>>     serialize=base64.b64encode,
>>>     parse_value=base64.b64decode
>>> )
```

```python
>>> @strawberry.scalar(
>>>     serialize=lambda value: ",".join(value.items),
>>>     parse_value=lambda value: CustomList(value.split(","))
>>> )
>>> class CustomList:
>>>     def __init__(self, items):
>>>         self.items = items
```

### strawberry.subscription(resolver=None, \*, name=None, is_subscription=True, description=None, permission_classes=None, deprecation_reason=None, default=UNSET, default_factory=UNSET, directives=(), init=None)

Annotates a method or property as a GraphQL field.

This is normally used inside a type declaration:

```python
>>> @strawberry.type:
>>> class X:
>>>     field_abc: str = strawberry.field(description="ABC")
```

```python
>>>     @strawberry.field(description="ABC")
>>>     def field_with_resolver(self) -> str:
>>>         return "abc"
```

it can be used both as decorator and as a normal function.

### strawberry.type(cls=None, \*, name=None, is_input=False, is_interface=False, description=None, directives=(), extend=False)

Annotates a class as a GraphQL type.

Example usage:

```python
>>> @strawberry.type:
>>> class X:
>>>     field_abc: str = "ABC"
```

### strawberry.union(name: str, types: Tuple[strawberry.union.Types, ...], \*, description: Optional[str] = None)

Creates a new named Union type.

Example usages:

```python
>>> @strawberry.type
... class A: ...
>>> @strawberry.type
... class B: ...
>>> strawberry.union("Name", (A, Optional[B]))
```
