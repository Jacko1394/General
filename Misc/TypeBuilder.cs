// TypeBuilder.cs
// MAGIQ Mobile
// Created by Jack Della on 12/10/2019
// Copyright © 2019 MAGIQ Software Ltd. All rights reserved.
using System;
using System.Reflection;
using System.Reflection.Emit;
using System.Collections.Generic;

#nullable enable

namespace Magiq.Mobile.Services {

	internal class CreateTableRequest {
		public List<Tuple<string, string>> Strings { get; set; } = new List<Tuple<string, string>>();
		public List<Tuple<string, long>> Numbers { get; set; } = new List<Tuple<string, long>>();
		public List<Tuple<string, bool>> Booleans { get; set; } = new List<Tuple<string, bool>>();
	}

	internal static class MyTypeBuilder {

		public static object? CreateNewObject(CreateTableRequest request) {

			var myTypeInfo = CompileResultTypeInfo(request);
			var myType = myTypeInfo?.AsType();

			if (myType is null) return null;

			var myObject = Activator.CreateInstance(myType);

			foreach (var item in request.Strings) {
				myObject.GetType().GetProperty(item.Item1)?.SetValue(myObject, item.Item2);
			}
			foreach (var item in request.Numbers) {
				myObject.GetType().GetProperty(item.Item1)?.SetValue(myObject, item.Item2);
			}
			foreach (var item in request.Booleans) {
				myObject.GetType().GetProperty(item.Item1)?.SetValue(myObject, item.Item2);
			}

			return myObject;

		}

		private static TypeInfo? CompileResultTypeInfo(CreateTableRequest request) {
			var tb = GetTypeBuilder();
			tb.DefineDefaultConstructor(MethodAttributes.Public | MethodAttributes.SpecialName | MethodAttributes.RTSpecialName);

			foreach (var item in request.Strings) {
				CreateProperty(tb, item.Item1, typeof(string));
			}
			foreach (var item in request.Numbers) {
				CreateProperty(tb, item.Item1, typeof(int));
			}
			foreach (var item in request.Booleans) {
				CreateProperty(tb, item.Item1, typeof(bool));
			}

			var objectTypeInfo = tb.CreateTypeInfo();
			return objectTypeInfo;
		}

		private static TypeBuilder GetTypeBuilder() {
			var typeSignature = "MyDynamicType";
			var an = new AssemblyName(typeSignature);
			var assemblyBuilder = AssemblyBuilder.DefineDynamicAssembly(an, AssemblyBuilderAccess.Run);
			var moduleBuilder = assemblyBuilder.DefineDynamicModule("MainModule");
			var tb = moduleBuilder.DefineType(typeSignature,
					TypeAttributes.Public |
					TypeAttributes.Class |
					TypeAttributes.AutoClass |
					TypeAttributes.AnsiClass |
					TypeAttributes.BeforeFieldInit |
					TypeAttributes.AutoLayout,
					null);
			return tb;
		}

		private static void CreateProperty(TypeBuilder tb, string propertyName, Type propertyType) {
			var fieldBuilder = tb.DefineField("_" + propertyName, propertyType, FieldAttributes.Private);

			var propertyBuilder = tb.DefineProperty(propertyName, PropertyAttributes.HasDefault, propertyType, null);
			var getPropMthdBldr = tb.DefineMethod("get_" + propertyName, MethodAttributes.Public | MethodAttributes.SpecialName | MethodAttributes.HideBySig, propertyType, Type.EmptyTypes);
			var getIl = getPropMthdBldr.GetILGenerator();

			getIl.Emit(OpCodes.Ldarg_0);
			getIl.Emit(OpCodes.Ldfld, fieldBuilder);
			getIl.Emit(OpCodes.Ret);

			var setPropMthdBldr =
				tb.DefineMethod("set_" + propertyName,
				  MethodAttributes.Public |
				  MethodAttributes.SpecialName |
				  MethodAttributes.HideBySig,
				  null, new[] { propertyType });

			var setIl = setPropMthdBldr.GetILGenerator();
			var modifyProperty = setIl.DefineLabel();
			var exitSet = setIl.DefineLabel();

			setIl.MarkLabel(modifyProperty);
			setIl.Emit(OpCodes.Ldarg_0);
			setIl.Emit(OpCodes.Ldarg_1);
			setIl.Emit(OpCodes.Stfld, fieldBuilder);

			setIl.Emit(OpCodes.Nop);
			setIl.MarkLabel(exitSet);
			setIl.Emit(OpCodes.Ret);

			propertyBuilder.SetGetMethod(getPropMthdBldr);
			propertyBuilder.SetSetMethod(setPropMthdBldr);
		}
	}
}
